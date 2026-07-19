import subprocess
import json
import os
import time

SIGNAL = r"C:\Users\user\Documents\signal-cli-0.14.6\bin\signal-cli.bat"
BOT_NUMBER = "+821032696753"
TARGET_GROUP_ID = "kjZINZM+f425T4BwODI5gALkd58kB+RfOi7e4Xwp8DE="

def listen_and_fast_trigger(account_number):
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    
    command = [SIGNAL, "-u", account_number, "jsonRpc"]
    
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        shell=True,
        env=env
    )
    
    # timeout: 1 옵션으로 실시간 동기화 강제 유도
    receive_request = {
        "jsonrpc": "2.0", 
        "method": "receive", 
        "params": {"timeout": 1}, 
        "id": "listen_mode"
    }
    proc.stdin.write((json.dumps(receive_request) + "\n").encode('utf-8'))
    proc.stdin.flush()
    
    print(f"⚡ [상시 감지] 내가 보낸 메시지 포함 실시간 모니터링 중... (대상 방: {TARGET_GROUP_ID})")

    # 멘션 데이터 사전에 빌드
    all_uuids = [
        ####PUT YOUR UUID'S HERE####
    ]

    mention_text = ""
    mentions_string_list = []
    
    for uuid in all_uuids:
        start_index = len(mention_text)
        tag = "@유저 "
        mention_text += tag
        mentions_string_list.append(f"{start_index}:{len(tag)-1}:{uuid}")
        
    start_index = len(mention_text)
    tag = "@나 "
    mention_text += tag
    mentions_string_list.append(f"{start_index}:{len(tag)-1}:{account_number}")
    
    final_message = f"{mention_text}\n\n "

    try:
        buffer = b""
        while True:
            char = proc.stdout.read(1)
            if not char:
                break
            buffer += char
            
            if char == b'\n':
                try:
                    decoded_line = buffer.decode('utf-8', errors='replace').strip()
                    buffer = b"" 
                    
                    if not decoded_line.startswith('{'):
                        continue
                        
                    data = json.loads(decoded_line)
                    
                    if "params" in data and "envelope" in data["params"]:
                        envelope = data["params"]["envelope"]
                        
                        # 🔍 메시지 추출 대상 초기화
                        data_message = None
                        
                        # 케이스 1: 다른 사람이 보낸 일반 메시지
                        if "dataMessage" in envelope:
                            data_message = envelope["dataMessage"]
                        # 케이스 2: ⭐ 내가 다른 기기(모바일/PC앱)에서 보낸 동기화 메시지
                        elif "syncMessage" in envelope and "sentMessage" in envelope["syncMessage"]:
                            data_message = envelope["syncMessage"]["sentMessage"]
                        
                        if data_message:
                            message_text = data_message.get("message", "")
                            
                            # @everyone이 텍스트에 포함되어 있다면
                            if "@everyone" in message_text:
                                group_info = data_message.get("groupInfo")
                                
                                if group_info and group_info.get("groupId") == TARGET_GROUP_ID:
                                    print(f"\n🚀 [@everyone 감지 완료! 즉시 멘션 발송]")
                                    
                                    # 열려있는 파이프에 즉시 전송 명령 전달
                                    send_payload = {
                                        "jsonrpc": "2.0",
                                        "method": "send",
                                        "params": {
                                            "groupId": TARGET_GROUP_ID,
                                            "message": final_message,
                                            "mentions": mentions_string_list
                                        },
                                        "id": f"fast_send_{int(time.time())}"
                                    }
                                    
                                    send_bytes = (json.dumps(send_payload, ensure_ascii=False) + "\n").encode('utf-8')
                                    proc.stdin.write(send_bytes)
                                    proc.stdin.flush()
                                    print("📢 멘션 직통 전송 완료.")
                                    
                except Exception:
                    buffer = b""
                    continue
                    
    except KeyboardInterrupt:
        print("\n🛑 감지 서버를 종료합니다.")
    finally:
        proc.terminate()

if __name__ == "__main__":
    listen_and_fast_trigger(BOT_NUMBER)
