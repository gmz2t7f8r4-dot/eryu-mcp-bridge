import json, os, urllib.request, urllib.parse
from mcp.server.fastmcp import FastMCP

ERYU_URL = os.environ.get("ERYU_URL", "").rstrip("/")
ERYU_TOKEN = os.environ.get("ERYU_TOKEN", "")
mcp = FastMCP("eryu-bridge", host="0.0.0.0", port=int(os.environ.get("PORT", "3000")))

def _api(path, method="GET", body=None):
    req = urllib.request.Request(ERYU_URL + path, method=method,
        headers={"X-Auth-Token": ERYU_TOKEN, "Content-Type": "application/json"},
        data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

@mcp.tool()
def search_song(keyword: str) -> str:
    """搜歌，返回 {id,name,artist,album,cover} 列表"""
    return json.dumps(_api("/music/search?q=" + urllib.parse.quote(keyword)), ensure_ascii=False)

@mcp.tool()
def get_lyric(song_id: int) -> str:
    """拿歌词和翻译"""
    return json.dumps(_api(f"/music/lyric?id={song_id}"), ensure_ascii=False)

@mcp.tool()
def get_recent() -> str:
    """看她最近听了什么"""
    return json.dumps(_api("/music/recent"), ensure_ascii=False)

@mcp.tool()
def get_playlists() -> str:
    """列出所有播放列表"""
    return json.dumps(_api("/music/playlists"), ensure_ascii=False)

@mcp.tool()
def get_daily() -> str:
    """每日推荐"""
    return json.dumps(_api("/music/daily"), ensure_ascii=False)

@mcp.tool()
def roam() -> str:
    """随机推荐一首歌"""
    return json.dumps(_api("/music/roam"), ensure_ascii=False)

@mcp.tool()
def get_stats() -> str:
    """听歌统计"""
    return json.dumps(_api("/music/stats"), ensure_ascii=False)

@mcp.tool()
def analyze_song(song_id: int, name: str = "", artist: str = "") -> str:
    """触发频谱分析（BPM/调性/能量曲线），后台跑，要等一会"""
    return json.dumps(_api("/music/analyze", method="POST",
        body={"songId": song_id, "name": name, "artist": artist}), ensure_ascii=False)

@mcp.tool()
def get_analysis(song_id: int) -> str:
    """查分析结果：duration/bpm/key/segments/spectrogram"""
    return json.dumps(_api(f"/music/analyze/status?id={song_id}"), ensure_ascii=False)

@mcp.tool()
def push_song(song_id: int, name: str, artist: str = "", cover: str = "", album: str = "") -> str:
    """推歌给她——网页播放器会自动开始放这首"""
    return json.dumps(_api("/music/remote", method="POST",
        body={"song": {"songId": song_id, "name": name, "artist": artist, "cover": cover, "album": album}}), ensure_ascii=False)

if __name__ == "__main__":
    mcp.run(transport="sse")
