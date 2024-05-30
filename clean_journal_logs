为了在公司电脑每天早上9点自动运行清理脚本，你可以设置一个系统定时任务。在 Ubuntu 上，你可以使用 `cron` 来实现这个功能。以下是详细步骤：

### 步骤1：创建清理脚本
首先，创建一个清理日志的脚本文件，确保它可以执行：

1. 打开终端，创建脚本文件：

   ```sh
   nano ~/clean_journal_logs.sh
   ```

2. 将以下脚本内容复制到文件中：

   ```bash
   #!/bin/bash

   # 定义日志保留时间和最大日志大小
   RETENTION_DAYS=7
   MAX_LOG_SIZE=500M

   echo "Cleaning journal logs..."

   # 清理旧日志，保留最近 $RETENTION_DAYS 天的日志
   sudo journalctl --vacuum-time=${RETENTION_DAYS}d

   # 清理旧日志，保留最多 $MAX_LOG_SIZE 的日志
   sudo journalctl --vacuum-size=$MAX_LOG_SIZE

   echo "Journal logs cleaned. Retention days: $RETENTION_DAYS, Max log size: $MAX_LOG_SIZE"
   ```

3. 保存并退出编辑器。

4. 赋予脚本执行权限：

   ```sh
   chmod +x ~/clean_journal_logs.sh
   ```

### 步骤2：编辑 `cron` 任务
设置一个 `cron` 任务，使其每天上午9点自动运行脚本：

1. 打开 `cron` 编辑器：

   ```sh
   crontab -e
   ```

2. 在 `crontab` 文件中添加以下行：

   ```sh
   0 9 * * * /path/to/your/home/directory/clean_journal_logs.sh
   ```

   将 `/path/to/your/home/directory/` 替换为你的实际用户主目录路径。例如，如果你的用户名是 `user`，路径应该是 `/home/user/clean_journal_logs.sh`。

3. 保存并退出编辑器。

### 步骤3：处理 `sudo` 权限
因为脚本中使用了 `sudo`，你需要配置 `sudo` 使其在执行时不需要密码。这可以通过编辑 `sudoers` 文件来实现。

1. 打开 `sudoers` 文件进行编辑：

   ```sh
   sudo visudo
   ```

2. 在文件末尾添加以下行，允许你的用户在执行该脚本时无需输入密码：

   ```sh
   your_username ALL=(ALL) NOPASSWD: /path/to/your/home/directory/clean_journal_logs.sh
   ```

   将 `your_username` 替换为你的实际用户名，`/path/to/your/home/directory/clean_journal_logs.sh` 替换为实际脚本路径。

3. 保存并退出编辑器。

### 验证
你可以通过以下方法验证 `cron` 任务是否设置正确：

1. 手动运行脚本，确保没有权限问题：

   ```sh
   ./clean_journal_logs.sh
   ```

2. 查看 `cron` 日志，确保任务按计划运行：

   ```sh
   grep CRON /var/log/syslog
   ```

通过这些步骤，你的电脑将在每天上午9点自动运行清理日志的脚本，保持系统的日志文件在合理范围内。
