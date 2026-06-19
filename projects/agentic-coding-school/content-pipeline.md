# Content Pipeline

Filter the whole content lifecycle from one note, regardless of which folder a script sits in. Stage is the `status` field (`idea → scripted → filmed`); `video_id` implies `filmed`. Requires the **Dataview** community plugin; until it's enabled these render as inert code blocks.

## Ideas (seeds & stubs — need scripting or a class)
```dataview
TABLE class AS "Class", file.folder AS "Folder"
FROM "projects/agentic-coding-school"
WHERE status = "idea"
SORT class ASC, file.name ASC
```

## To Film (scripted, not yet recorded)
```dataview
TABLE class AS "Class", file.folder AS "Folder"
FROM "projects/agentic-coding-school"
WHERE status = "scripted" AND !video_id
SORT class ASC, file.name ASC
```

## Filmed (in the database)
```dataview
TABLE class AS "Class", video_id AS "Video"
FROM "projects/agentic-coding-school"
WHERE video_id
SORT class ASC, file.name ASC
```

## Classless ideas (assign a class next)
```dataview
LIST
FROM "projects/agentic-coding-school"
WHERE status = "idea" AND !class
SORT file.name ASC
```

## Counts by stage
```dataview
TABLE length(rows) AS "Count"
FROM "projects/agentic-coding-school"
WHERE status
GROUP BY status
```
