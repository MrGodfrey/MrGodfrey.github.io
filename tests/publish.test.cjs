const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { test } = require('node:test');
const { publish } = require('../scripts/publish.cjs');

function fixture(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'homepage-publish-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  const remote = path.join(directory, 'remote.git');
  const cwd = path.join(directory, 'website');
  fs.mkdirSync(cwd);
  const git = (...args) => execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  git('init', '--bare', '--initial-branch=master', remote);
  git('init', '--initial-branch=master');
  git('config', 'user.name', 'Publish Test');
  git('config', 'user.email', 'test@example.invalid');
  git('config', 'commit.gpgsign', 'false');
  git('remote', 'add', 'origin', remote);
  fs.writeFileSync(path.join(cwd, 'package.json'), JSON.stringify({ scripts: { build: 'node build.cjs' } }));
  fs.writeFileSync(path.join(cwd, 'build.cjs'), "const fs = require('node:fs'); fs.writeFileSync('site.html', fs.readFileSync('content.txt'));\n");
  fs.writeFileSync(path.join(cwd, 'content.txt'), 'Initial content');
  git('add', '.');
  git('commit', '-m', 'Initial commit');
  git('push', 'origin', 'master');
  const remoteHead = () => git('--git-dir=' + remote, 'rev-parse', 'master');
  return { cwd, remote, git, remoteHead };
}

test('builds changed content, commits generated output, pushes and supports an unchanged rerun', t => {
  const { cwd, git, remoteHead } = fixture(t);
  fs.writeFileSync(path.join(cwd, 'content.txt'), 'Updated content');
  fs.writeFileSync(path.join(cwd, '.DS_Store'), 'not part of website');
  fs.mkdirSync(path.join(cwd, 'img'));
  fs.writeFileSync(path.join(cwd, 'img', '.DS_Store'), 'also excluded');
  const message = 'Update notes with literal `ticks` and $(text)';
  publish(cwd, message);
  assert.equal(git('show', 'HEAD:site.html'), 'Updated content');
  assert.equal(git('log', '-1', '--format=%B'), message);
  assert.equal(git('ls-files', '*DS_Store'), '');
  assert.equal(remoteHead(), git('rev-parse', 'HEAD'));
  const first = remoteHead();
  publish(cwd);
  assert.equal(remoteHead(), first);
});

test('build failure preserves source edits without committing or pushing them', t => {
  const { cwd, git, remoteHead } = fixture(t);
  const original = remoteHead();
  fs.writeFileSync(path.join(cwd, 'build.cjs'), 'process.exit(1);');
  assert.throws(() => publish(cwd), /npm run build/);
  assert.equal(git('rev-parse', 'HEAD'), original);
  assert.equal(remoteHead(), original);
  assert.match(git('status', '--short'), /build.cjs/);
});

test('remote commits missing locally stop publication before the build', t => {
  const { cwd, git, remoteHead } = fixture(t);
  const original = remoteHead();
  fs.writeFileSync(path.join(cwd, 'remote-change.txt'), 'Remote update');
  git('add', '.');
  git('commit', '-m', 'Remote update');
  git('push', 'origin', 'master');
  const advanced = remoteHead();
  git('reset', '--hard', original);
  assert.throws(() => publish(cwd), /远端 master 有本地未包含的提交/);
  assert.equal(remoteHead(), advanced);
  assert.equal(git('rev-parse', 'HEAD'), original);
  assert.equal(fs.existsSync(path.join(cwd, 'site.html')), false);
});

test('a rejected push keeps the local commit and a later rerun publishes it', t => {
  const { cwd, remote, git, remoteHead } = fixture(t);
  const original = remoteHead();
  const hook = path.join(remote, 'hooks', 'pre-receive');
  fs.writeFileSync(hook, '#!/bin/sh\nexit 1\n', { mode: 0o755 });
  assert.throws(() => publish(cwd), /git push/);
  const local = git('rev-parse', 'HEAD');
  assert.notEqual(local, original);
  assert.equal(remoteHead(), original);
  fs.unlinkSync(hook);
  publish(cwd);
  assert.equal(remoteHead(), local);
  assert.equal(git('rev-parse', 'HEAD'), local);
});
