#!/usr/bin/env node

// Build and publish this static site to the existing GitHub Pages branch.
const { spawnSync } = require('node:child_process');
const path = require('node:path');

function publish(cwd, message = 'Update academic homepage') {
  function run(command, args, capture = false) {
    const result = spawnSync(command, args, {
      cwd,
      encoding: 'utf8',
      stdio: capture ? 'pipe' : 'inherit',
    });
    if (result.error) throw result.error;
    if (result.status !== 0) {
      throw new Error(`${command} ${args.join(' ')} 执行失败。${capture ? '\n' + result.stderr : ''}`);
    }
    return capture ? result.stdout.trim() : undefined;
  }

  const branch = run('git', ['branch', '--show-current'], true);
  if (branch !== 'master') {
    throw new Error(`当前分支是 ${branch || '(detached HEAD)'}；请在 master 分支执行发布。`);
  }
  if (run('git', ['diff', '--name-only', '--diff-filter=U'], true)) {
    throw new Error('请先解决 Git 合并冲突，再执行发布。');
  }
  const stagedFiles = run('git', ['diff', '--cached', '--name-only', '-z'], true).split('\0');
  if (stagedFiles.some(file => path.basename(file) === '.DS_Store')) {
    throw new Error('暂存区含有 .DS_Store，请先取消暂存该文件，再执行发布。');
  }

  console.log('\n检查远端 master…');
  run('git', ['fetch', 'origin', 'master']);
  const ancestry = spawnSync('git', ['merge-base', '--is-ancestor', 'FETCH_HEAD', 'HEAD'], { cwd });
  if (ancestry.error) throw ancestry.error;
  if (ancestry.status === 1) {
    throw new Error('远端 master 有本地未包含的提交。请先合并远端更改，再重新发布。');
  }
  if (ancestry.status !== 0) throw new Error('无法检查远端提交，发布已停止。');

  console.log('\n构建网站与 PDF CV…');
  run('npm', ['run', 'build']);

  console.log('\n提交网站修改…');
  run('git', ['add', '--all', '--', '.', ':(glob,exclude)**/.DS_Store']);
  if (run('git', ['diff', '--cached', '--name-only'], true)) {
    run('git', ['diff', '--cached', '--stat']);
    run('git', ['commit', '-m', message]);
  } else {
    console.log('没有新的文件变化，跳过 commit。');
  }

  console.log('\n推送到 origin/master…');
  run('git', ['push', 'origin', 'HEAD:master']);
  const commit = run('git', ['rev-parse', '--short', 'HEAD'], true);
  console.log(`\n已推送 ${commit}。GitHub Pages 将自动更新线上页面。`);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) {
    console.log('用法：npm run deploy [-- "提交说明"]\n自动构建（含 PDF CV）、提交所有未被忽略的网站修改、推送 master。');
  } else {
    try {
      publish(path.resolve(__dirname, '..'), args.join(' ').trim() || undefined);
    } catch (error) {
      console.error(`\n发布未完成：${error.message}\n修复问题后可以重新运行 npm run deploy。`);
      process.exitCode = 1;
    }
  }
}

module.exports = { publish };
