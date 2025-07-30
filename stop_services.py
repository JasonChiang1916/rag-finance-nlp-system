#!/usr/bin/env python3
"""
服务停止脚本
优雅地停止所有相关服务并清理锁文件
"""

import os
import subprocess
import signal
import time

def find_processes():
    """查找相关进程"""
    processes = []
    
    try:
        # 查找 Python main.py 进程
        result = subprocess.run(['pgrep', '-f', 'python.*main.py'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            processes.extend(result.stdout.strip().split('\n'))
    except:
        pass
    
    try:
        # 查找 milvus 进程
        result = subprocess.run(['pgrep', 'milvus'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            processes.extend(result.stdout.strip().split('\n'))
    except:
        pass
    
    try:
        # 查找占用数据库文件的进程
        result = subprocess.run(['lsof', '+c', '0'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'financial_terms' in line and '.db' in line:
                parts = line.split()
                if len(parts) > 1:
                    processes.append(parts[1])
    except:
        pass
    
    return list(set(processes))  # 去重

def stop_processes(processes):
    """停止进程"""
    for pid in processes:
        try:
            pid = int(pid)
            print(f"🔄 停止进程 {pid}...")
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
            
            # 检查进程是否还在运行
            try:
                os.kill(pid, 0)  # 检查进程是否存在
                print(f"⚠️  进程 {pid} 未响应 SIGTERM，使用 SIGKILL...")
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                print(f"✅ 进程 {pid} 已停止")
        except (ValueError, ProcessLookupError):
            continue
        except PermissionError:
            print(f"❌ 没有权限停止进程 {pid}")

def clean_lock_files():
    """清理锁文件"""
    lock_patterns = [
        'backend/db/.*.db.lock',
        '/tmp/tmp*financial_terms*.sock'
    ]
    
    for pattern in lock_patterns:
        try:
            result = subprocess.run(['find', '.', '-name', pattern.split('/')[-1]], 
                                  capture_output=True, text=True)
            for lock_file in result.stdout.strip().split('\n'):
                if lock_file and os.path.exists(lock_file):
                    os.remove(lock_file)
                    print(f"🧹 清理锁文件: {lock_file}")
        except:
            pass

def main():
    print("🛑 停止金融术语标准化系统服务...")
    print("=" * 50)
    
    # 查找进程
    processes = find_processes()
    if processes:
        print(f"📋 发现 {len(processes)} 个相关进程")
        stop_processes(processes)
    else:
        print("✅ 没有发现运行中的相关进程")
    
    # 清理锁文件
    print("\n🧹 清理锁文件...")
    clean_lock_files()
    
    print("\n✅ 服务停止完成！")
    print("💡 现在可以安全地重新启动服务了")

if __name__ == "__main__":
    main()
