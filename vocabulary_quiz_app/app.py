from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        self.root= root
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("420x280")
        root.resizable(False, False)

        # 엔터 누를때 정답이 적혀있으면 채점, 없으면 다음으로 넘어감 그리고 한번 더 누르면 다음 단어로 넘어감
        root.bind("<Return>", lambda event: self.check_current() if not self.checked else self.next_word())
        
        self.setup_timer()

        self.word_var = tk.StringVar(value="단어를 불러오는 중...")
        self.feedback_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="Score: 0/0")

        ttk.Label(root, text="영단어").pack(pady=(16, 4))
        ttk.Label(root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.answer_entry = ttk.Entry(root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=12, ipadx=6, ipady=4)

        buttons = ttk.Frame(root)
        buttons.pack(pady=6)
        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="다음", command=self.next_word).pack(
            side=tk.LEFT, padx=6
        )

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()

        self.next_word()

    def next_word(self) -> None:
        self.current = draw_word(self.words, self.rng)
        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

        #단어 넘어갈때마다 타이머 시작
        self.reset_and_start_timer()

    def check_current(self) -> None:
        if self.current is None or self.checked:
            return
        self.checked = True

        # 사용자가 답을 제출하면 카운트 멈춤
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        
        self.total += 1
        user_input = self.answer_entry.get()
        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            self.feedback_var.set(f"오답입니다. 정답: {self.current.meaning}")
        self.score_var.set(f"Score: {self.score}/{self.total}")
        self.check_button.state(["disabled"])

    #타이머 세팅
    def setup_timer(self) -> None:
        self.time_limit=10
        self.time_left=self.time_limit
        self.timer_job=None #타이머 이벤트 취소 변수 

        #타이머 글자 변수 생성 및 ui 배치
        self.time_var = tk.StringVar(value=f"남은 시간: {self.time_left}")
        ttk.Label(self.root, textvariable=self.time_var, font=("NanumGothic", 12, "bold"), foreground="red").pack(pady=(10, 0))

    #타이머 리셋하고 다시 시작하는 함수
    def reset_and_start_timer(self) -> None:
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.time_left = self.time_limit
        self.time_var.set(f"남은 시간: {self.time_left}초")
        self.update_timer()

    # 카운트 다운 함수
    def update_timer(self) -> None:
        if self.checked: #채점이 완료된 상태면 타이머 정지
            return
        if self.time_left > 0:
            self.time_left -= 1
            self.time_var.set(f"남은 시간: {self.time_left}초")
            self.timer_job = self.root.after(1000, self.update_timer) 
        else:
            self.time_var.set("시간 초과!")
            self.handle_timeout()

    # 0초 되면 오답 처리 함수
    def handle_timeout(self) -> None:
        if self.current is None or self.checked:
            return
        self.checked = True
        self.total += 1
        self.feedback_var.set(f"시간이 초과되었습니다! 정답: {self.current.meaning}")
        self.score_var.set(f"Score: {self.score}/{self.total}")
        self.check_button.state(["disabled"])