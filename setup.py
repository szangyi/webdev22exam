from bottle import request, default_app
import git

application = default_app()

application.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin
        origin.pull()
    return 'Updated PythonAnywhere successfully'
