import sqlite3


conn = sqlite3.connect('data/data.db')
c = conn.cursor()


class BuildTarget:
    def __init__(self, id, git_branch, git_commit, buildtarget_id, buildtarget_name):
        self.id = id
        self.git_branch = git_branch
        self.git_commit = git_commit
        self.buildtarget_id = buildtarget_id
        self.buildtarget_name = buildtarget_name

    @staticmethod
    def ensure_table():
        c.execute('''CREATE TABLE IF NOT EXISTS buildtargets(
                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     git_branch TEXT,
                     git_commit TEXT,
                     buildtarget_id TEXT,
                     buildtarget_name TEXT)''')

    @staticmethod
    def create(git_branch, git_commit, buildtarget_id, buildtarget_name):
        build_target = BuildTarget(None, git_branch, git_commit, buildtarget_id, buildtarget_name)
        build_target.save()

    @staticmethod
    def find(**kwargs):
        query = 'SELECT * FROM buildtargets WHERE'
        values = []
        for field, value in kwargs.items():
            query += ' {}=?'.format(field)
            values.append(value)
        c.execute(query, values)
        row = c.fetchone()
        return BuildTarget(*row)

    def save(self):
        with conn:
            if self.id:
                self._save_updated()
            else:
                self._save_new()

    def _save_new(self):
        values = (self.git_branch, self.git_commit, self.buildtarget_id, self.buildtarget_name)
        c.execute('INSERT INTO buildtargets VALUES (NULL, ?, ?, ?, ?)', values)

    def _save_updated(self):
        values = (self.git_branch, self.git_commit, self.buildtarget_id, self.buildtarget_name, self.id)
        c.execute('''UPDATE buildtargets
                     SET git_branch=?, git_commit=?, buildtarget_id=?, buildtarget_name=?
                     WHERE id=?''', values)

    def delete(self):
        with conn:
            c.execute('DELETE FROM buildtargets WHERE id=?', (self.id,))


BuildTarget.ensure_table()
