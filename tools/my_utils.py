import platform,os,traceback
import ffmpeg
import numpy as np


def load_audio(file, sr):
    try:
        # https://github.com/openai/whisper/blob/main/whisper/audio.py#L26
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        file = clean_path(file)  # 防止小白拷路径头尾带了空格和"和回车
        if os.path.exists(file) == False:
            raise RuntimeError(
                "You input a wrong audio path that does not exists, please fix it!"
            )
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f"Failed to load audio: {e}")

    return np.frombuffer(out, np.float32).flatten()


def clean_path(path_str):
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 将相对路径转换为绝对路径
    absolute_path = os.path.join(current_dir, os.path.normpath(path_str))
    return absolute_path
