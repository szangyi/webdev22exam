from bottle import request
import git

@app.route('/', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('path/to/git_repo')
            origin = repo.remotes.origin
origin.pull()
return 'Updated PythonAnywhere successfully'
