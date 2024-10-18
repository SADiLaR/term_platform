let env = process.env;

module.exports = {
    ci: {
        collect: {
            startServerCommand: `DB_NAME=test_db_1 DB_USER=sadilar DB_PASSWORD=sadilar`
                + "python manage.py runserver localhost:3000",
            url: [
                "http://localhost:3000",
                "http://localhost:3000/search/",
                "http://localhost:3000/institutions/",
                "http://localhost:3000/projects/",
                "http://localhost:3000/documents/",
                "http://localhost:3000/languages/",
                "http://localhost:3000/subjects/"
            ]
        },
        assert: {
            "preset": "lighthouse:recommended",
            "assertions": {
                // We are running this against a Django testing server
                "is-on-https": false,
            }
        }
    }
}

console.log(module.exports.ci.collect.startServerCommand)
