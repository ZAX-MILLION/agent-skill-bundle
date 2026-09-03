# Input Validation & Injection Security Gate

Use this reference for any attacker-controlled input that reaches SQL/NoSQL, shell commands, templates, HTML, URLs, redirects, filesystem paths, headers, regular expressions, or dynamic code/configuration.

## Validation model

- Validate at the server/trust boundary that consumes the input.
- Prefer allowlists over blocklists for enums, actions, fields, file types, protocols, hosts, sort keys, and operators.
- Apply length/range/count limits before expensive parsing or processing.
- Normalize before validating when equivalent encodings/case/path forms can bypass checks.
- Reject unexpected object keys when they could alter privilege or behavior.

## Injection families

### SQL / NoSQL / query injection

- Parameterize values through the database/ORM API.
- Never interpolate request values into raw query strings.
- Dynamic identifiers/operators/order-by clauses require explicit allowlists; placeholders usually do not protect identifiers.

### Command injection

- Avoid invoking a shell when a library/API can perform the operation directly.
- Prefer argument-array process APIs instead of command-string concatenation.
- Never pass attacker-controlled strings to `sh -c`, `bash -c`, `eval`, PowerShell expression evaluation, or equivalent without a narrowly reviewed design.

### Template / code execution

- Do not evaluate user-controlled templates/code/expressions in a privileged runtime.
- Avoid `eval`, `new Function`, dynamic imports from user paths, unsafe deserialization, or equivalent execution shortcuts.
- If user-supplied code is a product feature, isolate it in a deliberate sandbox with resource/network/secret boundaries.

### XSS / HTML injection

- Use framework escaping by default.
- Avoid raw HTML sinks such as `dangerouslySetInnerHTML` unless genuinely required.
- Sanitize user-controlled HTML with a maintained sanitizer and a restrictive allowlist policy.
- Treat URL/attribute/CSS/script contexts separately; generic HTML escaping is not always sufficient for every sink.

### Path traversal

- Resolve against an allowed root and verify the final canonical path remains inside it.
- Reject absolute paths, traversal segments, encoded traversal, and unsafe archive extraction paths.
- Generate server-side filenames/object keys rather than trusting uploads' original names as paths.

### Header / response splitting / redirects

- Never inject untrusted CR/LF into response headers.
- Validate redirect destinations against an allowlist or safe relative-path policy.
- Do not reflect arbitrary user input into security-sensitive headers.

### ReDoS / parser abuse

- Avoid unbounded attacker-controlled regular expressions or nested parsing that can cause pathological CPU/memory use.
- Set body/file/decompression limits before processing.

## Adversarial payload thinking

Use safe, non-destructive tests appropriate to the local environment. Consider:

- quotes/operators in query fields;
- shell metacharacters in command arguments;
- `../` plus encoded traversal variants;
- HTML/script/event-handler payloads in user-rendered fields;
- unexpected object keys and nested objects;
- CR/LF in header-bound input;
- external redirect targets;
- extreme lengths, nesting, regex complexity, decompression ratios.

## Release blockers

- attacker-controlled string concatenated into executable SQL/query/shell/template code;
- raw HTML rendered from untrusted data without a deliberate sanitizer policy;
- filesystem path built directly from user input without containment verification;
- arbitrary redirect/header injection;
- dynamic code execution from untrusted input;
- no meaningful bounds on expensive parser/regex/input processing exposed to attackers.
