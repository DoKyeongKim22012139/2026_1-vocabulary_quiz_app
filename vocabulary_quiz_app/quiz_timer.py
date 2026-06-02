import tkinter as tk
from tkinter import ttk

class QuizTimer:
    #타이머랑, 타이머가 끝났을때 실행할 함수 받기
    def __init__(self, root: tk.Tk, time_limit: int = 10, on_timeout = None) -> None:
        self.root = root
        self.time_limit = time_limit
        self.time_left = time_limit
        self.timer_job = None

        #시간 초과 시 퀴즈 앱이 실행할 함수를 받아둡니다.
        self.on_timeout = on_timeout 

        # 타이머 UI 배치
        self.time_var = tk.StringVar(value=f"남은 시간: {self.time_limit}초")
        self.label = ttk.Label(root, textvariable=self.time_var, font=("NanumGothic", 12, "bold"), foreground="red")
        self.label.pack(pady=(10, 0))

    def start(self) -> None:
        #새 문제 시작 시 타이머 리셋하고 시작
        self.stop() # 혹시 돌고 있을지 모를 이전 타이머 정지
        self.time_left = self.time_limit
        self.time_var.set(f"남은 시간: {self.time_left}초")
        self.update_timer()

    def stop(self) -> None:
        #정답을 맞추거나 채점했을때 타이머 멈추기
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def update_timer(self) -> None:
        #1초마다 카운타 깎는 함수
        if self.time_left > 0:
            self.time_left -= 1
            self.time_var.set(f"남은 시간: {self.time_left}초")
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.time_var.set("시간 초과!")
            if self.on_timeout:
                self.on_timeout() 