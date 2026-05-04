import SwiftUI
import AppKit
import Network
import Foundation

// MARK: - Model

struct SlideNote: Codable, Identifiable, Equatable {
    var id: Int
    var key: String
    var headline: String
    var caption: String
    var notes: String
}

struct NotesDoc: Codable, Equatable {
    var current: Int
    var slides: [SlideNote]
}

// MARK: - Notes file path

func notesFileURL() -> URL {
    // notes.json sits next to the SpeakerNotes folder in animations/slides/
    // Resolution priority:
    //   1. Working directory's notes.json (when run from animations/slides/)
    //   2. ../../notes.json from a build product inside .build/
    //   3. SPEAKER_NOTES_PATH env var
    if let env = ProcessInfo.processInfo.environment["SPEAKER_NOTES_PATH"] {
        return URL(fileURLWithPath: env)
    }
    let cwd = FileManager.default.currentDirectoryPath
    let candidates = [
        URL(fileURLWithPath: cwd).appendingPathComponent("notes.json"),
        URL(fileURLWithPath: cwd).appendingPathComponent("../notes.json"),
        URL(fileURLWithPath: cwd).appendingPathComponent("../../notes.json"),
    ]
    for c in candidates {
        if FileManager.default.fileExists(atPath: c.path) { return c }
    }
    return candidates[0]
}

// MARK: - Store

@MainActor
final class NotesStore: ObservableObject {
    @Published var doc: NotesDoc = NotesDoc(current: 0, slides: [])
    @Published var statusMessage: String = ""

    private let url: URL
    private var lastWrittenHash: String = ""
    private var saveWorkItem: DispatchWorkItem?
    private var fileWatcher: DispatchSourceFileSystemObject?

    init() {
        self.url = notesFileURL()
        load()
        startWatching()
    }

    func load() {
        do {
            let data = try Data(contentsOf: url)
            let decoded = try JSONDecoder().decode(NotesDoc.self, from: data)
            self.doc = decoded
            self.lastWrittenHash = String(data: data, encoding: .utf8) ?? ""
            self.statusMessage = "loaded \(url.lastPathComponent)"
        } catch {
            self.statusMessage = "load failed: \(error.localizedDescription)"
        }
    }

    func saveDebounced() {
        saveWorkItem?.cancel()
        let item = DispatchWorkItem { [weak self] in
            Task { @MainActor in self?.saveNow() }
        }
        saveWorkItem = item
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5, execute: item)
    }

    func saveNow() {
        do {
            let enc = JSONEncoder()
            enc.outputFormatting = [.prettyPrinted, .sortedKeys]
            let data = try enc.encode(doc)
            try data.write(to: url, options: .atomic)
            self.lastWrittenHash = String(data: data, encoding: .utf8) ?? ""
            self.statusMessage = "saved \(timestamp())"
        } catch {
            self.statusMessage = "save failed: \(error.localizedDescription)"
        }
    }

    func setCurrent(_ idx: Int) {
        guard idx >= 0 && idx < doc.slides.count else { return }
        doc.current = idx
        saveNow()
    }

    func next() { setCurrent(min(doc.current + 1, doc.slides.count - 1)) }
    func prev() { setCurrent(max(doc.current - 1, 0)) }

    private func timestamp() -> String {
        let f = DateFormatter()
        f.dateFormat = "HH:mm:ss"
        return f.string(from: Date())
    }

    // file watch — react to deck POSTing to /current via the HTTP server (which we own)
    // and to direct file edits from outside.
    private func startWatching() {
        let fd = open(url.path, O_EVTONLY)
        guard fd >= 0 else { return }
        let src = DispatchSource.makeFileSystemObjectSource(
            fileDescriptor: fd,
            eventMask: [.write, .extend, .rename, .delete],
            queue: .main
        )
        src.setEventHandler { [weak self] in
            guard let self = self else { return }
            // re-load if disk content differs
            if let data = try? Data(contentsOf: self.url),
               let str = String(data: data, encoding: .utf8),
               str != self.lastWrittenHash,
               let decoded = try? JSONDecoder().decode(NotesDoc.self, from: data) {
                self.doc = decoded
                self.lastWrittenHash = str
                self.statusMessage = "reloaded \(self.timestamp())"
            }
        }
        src.setCancelHandler { close(fd) }
        src.resume()
        self.fileWatcher = src
    }
}

// MARK: - HTTP Server (NWListener, hand-rolled HTTP)

final class CurrentSyncServer {
    private var listener: NWListener?
    weak var store: NotesStore?

    func start(port: UInt16 = 7878) {
        do {
            let params = NWParameters.tcp
            let listener = try NWListener(using: params, on: NWEndpoint.Port(rawValue: port)!)
            self.listener = listener
            listener.newConnectionHandler = { [weak self] conn in
                self?.handle(conn)
            }
            listener.start(queue: .main)
        } catch {
            NSLog("server start failed: \(error)")
        }
    }

    private func handle(_ conn: NWConnection) {
        conn.start(queue: .main)
        conn.receive(minimumIncompleteLength: 1, maximumLength: 64 * 1024) { [weak self] data, _, _, _ in
            guard let self = self, let data = data, let req = String(data: data, encoding: .utf8) else {
                conn.cancel(); return
            }
            let response = self.respond(to: req)
            conn.send(content: response, completion: .contentProcessed { _ in conn.cancel() })
        }
    }

    private func respond(to request: String) -> Data {
        let lines = request.components(separatedBy: "\r\n")
        guard let firstLine = lines.first else { return httpResponse(status: 400, body: "bad") }
        let parts = firstLine.split(separator: " ")
        guard parts.count >= 2 else { return httpResponse(status: 400, body: "bad") }
        let method = String(parts[0])
        let path = String(parts[1])

        // CORS preflight + headers — the deck might be served from file:// or http://localhost
        if method == "OPTIONS" {
            return httpResponse(status: 204, body: "")
        }

        if path.hasPrefix("/current") {
            if method == "GET" {
                let cur = DispatchQueue.main.sync { self.store?.doc.current ?? 0 }
                return httpResponse(status: 200, body: "{\"current\":\(cur)}", contentType: "application/json")
            }
            if method == "POST" {
                // body after \r\n\r\n
                if let bodyRange = request.range(of: "\r\n\r\n") {
                    let body = String(request[bodyRange.upperBound...])
                    if let data = body.data(using: .utf8),
                       let obj = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                       let n = obj["current"] as? Int {
                        DispatchQueue.main.async {
                            self.store?.setCurrent(n)
                        }
                        return httpResponse(status: 200, body: "{\"ok\":true}", contentType: "application/json")
                    }
                }
                return httpResponse(status: 400, body: "{\"error\":\"bad body\"}", contentType: "application/json")
            }
        }
        return httpResponse(status: 404, body: "not found")
    }

    private func httpResponse(status: Int, body: String, contentType: String = "text/plain") -> Data {
        let statusText: String
        switch status {
        case 200: statusText = "OK"
        case 204: statusText = "No Content"
        case 400: statusText = "Bad Request"
        case 404: statusText = "Not Found"
        default:  statusText = "OK"
        }
        let bodyData = body.data(using: .utf8) ?? Data()
        let headers = """
        HTTP/1.1 \(status) \(statusText)\r
        Content-Type: \(contentType)\r
        Content-Length: \(bodyData.count)\r
        Access-Control-Allow-Origin: *\r
        Access-Control-Allow-Methods: GET, POST, OPTIONS\r
        Access-Control-Allow-Headers: Content-Type\r
        Connection: close\r
        \r

        """
        var out = headers.data(using: .utf8) ?? Data()
        out.append(bodyData)
        return out
    }
}

// MARK: - View

struct ContentView: View {
    @EnvironmentObject var store: NotesStore
    @State private var showMeta = false

    var body: some View {
        let idx = max(0, min(store.doc.current, max(0, store.doc.slides.count - 1)))
        VStack(spacing: 0) {
            // tiny header strip
            HStack(spacing: 8) {
                Button(action: { store.prev() }) {
                    Image(systemName: "chevron.left")
                }
                .buttonStyle(.borderless)
                .keyboardShortcut(.leftArrow, modifiers: .command)

                Text("\(store.doc.current + 1)/\(store.doc.slides.count)")
                    .font(.system(.caption, design: .monospaced))
                    .foregroundColor(.secondary)

                Button(action: { store.next() }) {
                    Image(systemName: "chevron.right")
                }
                .buttonStyle(.borderless)
                .keyboardShortcut(.rightArrow, modifiers: .command)

                if !store.doc.slides.isEmpty {
                    Text(store.doc.slides[idx].headline)
                        .font(.system(.caption))
                        .foregroundColor(.secondary)
                        .lineLimit(1)
                        .truncationMode(.tail)
                }

                Spacer()

                Button(action: { showMeta.toggle() }) {
                    Image(systemName: showMeta ? "chevron.up" : "ellipsis")
                }
                .buttonStyle(.borderless)
                .help("Toggle headline + caption editors")
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 6)
            .background(Color(NSColor.windowBackgroundColor))

            Divider()

            if !store.doc.slides.isEmpty {
                if showMeta {
                    VStack(spacing: 4) {
                        TextField("headline", text: Binding(
                            get: { store.doc.slides[idx].headline },
                            set: { store.doc.slides[idx].headline = $0; store.saveDebounced() }
                        ))
                        .textFieldStyle(.roundedBorder)
                        .font(.system(.callout))
                        TextField("caption", text: Binding(
                            get: { store.doc.slides[idx].caption },
                            set: { store.doc.slides[idx].caption = $0; store.saveDebounced() }
                        ))
                        .textFieldStyle(.roundedBorder)
                        .font(.system(.caption))
                    }
                    .padding(.horizontal, 8)
                    .padding(.top, 6)
                }

                TextEditor(text: Binding(
                    get: { store.doc.slides[idx].notes },
                    set: { store.doc.slides[idx].notes = $0; store.saveDebounced() }
                ))
                .id(idx)
                .font(.system(size: 17))
                .padding(8)
            } else {
                Text("no slides loaded")
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .frame(minWidth: 360, minHeight: 220)
    }
}

// MARK: - App

@MainActor
final class AppController {
    let store = NotesStore()
    let server = CurrentSyncServer()

    func start() {
        server.store = store
        server.start(port: 7878)

        let hosting = NSHostingController(rootView: ContentView().environmentObject(store))
        let window = NSWindow(contentViewController: hosting)
        window.setContentSize(NSSize(width: 460, height: 320))
        window.styleMask = [.titled, .closable, .miniaturizable, .resizable]
        window.title = "Speaker Notes"
        window.level = .floating

        // Hide from screen capture (ScreenCaptureKit + legacy CGWindow respect this)
        window.sharingType = .none

        window.center()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }
}

// MARK: - main

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)

class AppDelegate: NSObject, NSApplicationDelegate {
    var controller: AppController?
    func applicationDidFinishLaunching(_ notification: Notification) {
        let ctrl = AppController()
        ctrl.start()
        controller = ctrl
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
}

app.run()
