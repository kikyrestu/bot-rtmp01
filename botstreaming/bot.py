import subprocess
import time

def start_streaming(video_path, rtmp_url, ffmpeg_path):
    command = [
        ffmpeg_path,
        '-re',
        '-stream_loop', '-1',  # Loop the video indefinitely
        '-i', video_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-f', 'flv',
        rtmp_url
    ]
    return subprocess.Popen(command)

def main():
    ffmpeg_path = input("Masukkan path ffmpeg (contoh: /usr/bin/ffmpeg): ")
    video_path = input("Masukkan path video: ")
    num_accounts = int(input("Masukkan jumlah akun yang ingin live streaming (max 5): "))
    
    if num_accounts < 1 or num_accounts > 5:
        print("Jumlah akun harus antara 1 dan 5.")
        return

    servers = []
    for i in range(num_accounts):
        name = input(f"Masukkan nama untuk akun {i+1}: ")
        rtmp_server = input(f"Masukkan URL server RTMP untuk akun {i+1} (contoh: rtmp://server/app): ")
        stream_key = input(f"Masukkan stream key untuk akun {i+1}: ")
        rtmp_url = f"{rtmp_server}/{stream_key}"
        servers.append({'name': name, 'rtmp_url': rtmp_url})

    processes = []
    for server in servers:
        process = start_streaming(video_path, server['rtmp_url'], ffmpeg_path)
        processes.append((server['name'], process))
        print(f"Started streaming to {server['name']}")

    try:
        while True:
            for name, process in processes:
                if process.poll() is not None:
                    print(f"Stream to {name} has ended. Restarting...")
                    new_process = start_streaming(video_path, next(s['rtmp_url'] for s in servers if s['name'] == name), ffmpeg_path)
                    processes.append((name, new_process))
                    processes.remove((name, process))
            time.sleep(10)
    except KeyboardInterrupt:
        for name, process in processes:
            process.terminate()
            print(f"Stopped streaming to {name}")

if __name__ == "__main__":
    main()