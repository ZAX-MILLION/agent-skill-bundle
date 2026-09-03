# Uploads & Object Storage Security Gate

Use this reference for file uploads, media processing, document imports, archives, object storage, signed URLs, private downloads, or user-controlled filenames.

## Treat files as hostile input

- Enforce server-side size, count, type, and processing-cost limits.
- Do not trust the client MIME header or file extension alone.
- Use a content/magic-byte check when format trust matters.
- Prefer a narrow allowlist of formats the feature genuinely needs.
- Reject executable/server-script formats unless the product explicitly requires them and has an isolation design.

## Storage design

- Generate safe server-side object keys/filenames; do not use the original filename as a filesystem path.
- Keep user uploads outside executable application directories where possible.
- Private files belong in private storage. Public bucket/object URLs are not authorization.
- Download/read operations need the same ownership/tenant authorization as database records.
- Signed URLs should be short-lived and scoped to the exact intended object/action.

## Path and archive safety

- Resolve filesystem paths against a fixed allowed root and verify canonical containment.
- Reject traversal (`../`), absolute paths, encoded traversal, null-byte/path tricks, and unsafe separator variants.
- Archive extraction must block zip-slip/tar traversal and should bound file count/expanded size to resist decompression bombs.

## Media/document processing

- Image/PDF/video/document parsers are attack surfaces. Keep libraries patched and avoid unnecessary processing of arbitrary formats.
- Bound dimensions, pages, duration, archive depth, memory, CPU, and conversion time.
- Do not execute embedded macros/scripts.
- Consider malware/content scanning where the application's risk warrants it; scanning does not replace type/authorization controls.

## Serving files

- Set safe `Content-Type` and `Content-Disposition` as appropriate.
- Prevent uploaded active content from executing in the application's trusted origin where feasible.
- Do not reflect arbitrary filenames into headers without sanitization/encoding.
- Avoid cache settings that could expose private files to other users.

## Adversarial checks

- oversized file -> rejected;
- disallowed type or content/extension mismatch -> rejected;
- filename containing traversal -> cannot escape storage root;
- archive with traversal entry -> rejected;
- user A requests user B's private object/key -> rejected;
- anonymous caller cannot access private storage through guessed URLs;
- uploaded HTML/SVG/script-like content cannot execute under a trusted origin unless explicitly designed and isolated;
- signed URL expires and is scoped correctly.

## Release blockers

- unrestricted upload into executable/public application paths;
- private objects readable without authorization;
- original filenames used directly as filesystem paths;
- no upload size/type/processing limits;
- unsafe archive extraction;
- service/admin storage credential exposed to client code;
- private content cached or served as another user's response.
