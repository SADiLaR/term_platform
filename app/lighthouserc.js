module.exports = {
    ci: {
        collect: {
            // We don't care about variable page performance metrics in CI - just static asserts
            numberOfRuns: 1,
            startServerCommand: "../entrypoint.sh",
            url: [
                "http://localhost:8000",
                "http://localhost:8000/search/",
                "http://localhost:8000/institutions/",
                "http://localhost:8000/projects/",
                "http://localhost:8000/documents/",
                "http://localhost:8000/languages/",
                "http://localhost:8000/subjects/"
            ]
        },
        assert: {
            "preset": "lighthouse:recommended",
            "assertions": {
                // Gunicorn doesn't do this, but the reverse proxy in front of it does
                "uses-text-compression": false,

                // We don't think these are worth worrying about for now
                "unminified-javascript": false,
                "unused-css-rules": false,
                "unminified-css": false,
                "render-blocking-resources": false,
            }
        }
    }
}
