// Claude Code GrowthBook flag forcer
// Managed by the `ungate-claude-code-feature` skill.
//
// Proxyman scripting rule. Attach to URL:  https://api.anthropic.com/api/eval/*
// It rewrites the GrowthBook remote-eval response so the flags listed in FORCED
// resolve to the values you want, regardless of what Anthropic's server returns.
//
// To ungate another feature, add one entry to FORCED:
//   key   = the tengu_* flag name
//   value = a boolean for a simple on/off gate, OR an object for a config flag.
//           Objects are merged into the server's value so other fields survive.

var FORCED = {
  "tengu_review_bughunter_config": { "enabled": true },             // /ultrareview
  "tengu_kairos_brief_config":     { "enable_slash_command": true },
  "tengu_kairos_brief":            true,
  "tengu_workflows_enabled":       true                             // Workflow tool + /workflows
};

async function onRequest(context, url, request) {
  return request;
}

async function onResponse(context, url, request, response) {
  if (!url.includes("/api/eval/sdk-")) {
    return response;
  }
  try {
    var body = response.body;
    if (typeof body === "string") {
      body = JSON.parse(body);
    }
    if (body && body.features) {
      for (var key in FORCED) {
        var want = FORCED[key];
        var feat = body.features[key];
        if (feat && feat.value && typeof feat.value === "object" &&
            want && typeof want === "object") {
          // Merge so server-provided fields (timeouts, limits) are not lost.
          for (var f in want) { feat.value[f] = want[f]; }
          feat.on = true; feat.off = false; feat.source = "force";
        } else {
          body.features[key] = {
            "source": "force", "experiment": null, "on": true,
            "ruleId": null, "off": false, "value": want,
            "experimentResult": null
          };
        }
      }
    }
    response.body = JSON.stringify(body);
  } catch (e) {}
  return response;
}
