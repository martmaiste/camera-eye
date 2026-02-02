# Minimal NVR Health Probe v0.03
# Purpose: Added IP Address column and improved URL parsing
import yaml
import subprocess
import json
import os
import re

def extract_ip(url):
    # Regex to find an IPv4 address in a string
    ip_match = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    return ip_match.group(0) if ip_match else "Unknown"

def probe_stream(name, url):
    # Clean up go2rtc specific prefixes
    clean_url = url.replace("ffmpeg:", "").split("#")[0]
    ip_addr = extract_ip(clean_url)
    
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-rtsp_transport', 'tcp', 
        '-analyzeduration', '5000000',
        '-probesize', '5000000',
        '-select_streams', 'v:0', 
        '-show_entries', 'stream=codec_name,width,height,avg_frame_rate', 
        '-of', 'json', 
        clean_url
    ]
    
    print(f"Probing {name[:25]}...", end="\r")
    
    try:
        # 15s timeout for remote feeds
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            err = result.stderr if result.stderr else ""
            status = "OFFLINE"
            note = "Auth Failed" if "401" in err else "Conn. Failed"
            return {"status": status, "ip": ip_addr, "error": note}
        
        data = json.loads(result.stdout)
        if 'streams' in data and len(data['streams']) > 0:
            s = data['streams'][0]
            codec = s.get('codec_name', '-')
            codec_str = f"{codec} (!)" if codec == "hevc" else codec
            
            return {
                "status": "ONLINE",
                "ip": ip_addr,
                "codec": codec_str,
                "res": f"{s.get('width')}x{s.get('height')}",
                "fps": s.get('avg_frame_rate')
            }
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "ip": ip_addr, "error": "Remote timeout"}
    except Exception:
        return {"status": "ERROR", "ip": ip_addr, "error": "Internal Err"}
    
    return {"status": "UNKNOWN", "ip": ip_addr, "error": "No video"}

def main():
    config_path = 'config/go2rtc.yaml'
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    streams = config.get('streams', {})
    
    # Table Header with IP column
    header = f"{'CAMERA':<30} | {'IP ADDRESS':<15} | {'STATUS':<10} | {'RES':<12} | {'CODEC':<8} | {'INFO'}"
    print("\n" + header)
    print("-" * 110)

    for name, sources in streams.items():
        if isinstance(sources, list):
            for i, url in enumerate(sources):
                label = f"{name} ({'sub' if i==0 else 'main'})"
                info = probe_stream(label, url)
                print_row(label, info)
        else:
            info = probe_stream(name, sources)
            print_row(name, info)

def print_row(name, info):
    print(f"{name[:30]:<30} | {info['ip']:<15} | {info['status']:<10} | "
          f"{info.get('res', '-'):<12} | {info.get('codec', '-'):<8} | {info.get('error', info.get('fps', ''))}")

if __name__ == "__main__":
    main()
