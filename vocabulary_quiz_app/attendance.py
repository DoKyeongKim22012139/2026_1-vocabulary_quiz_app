from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

ATTENDANCE_FILE = Path("attendance.json") #json에 출석 정보저장


class AttendanceManager:
    def __init__(self) -> None:
        self.data = self._load()

    
    def update_streak(self) -> None:
        last_date_str = self.data["last_attendance"]

        if not last_date_str:
            return

        last_date = datetime.strptime(last_date_str,"%Y-%m-%d").date()

        diff = (date.today() - last_date).days

        #출석 연속 끊기면 바로 반영
        if diff >= 2:
            self.data["streak"] = 0
            self._save()


    def _load(self) -> dict:
        if not ATTENDANCE_FILE.exists(): #처음에 없으면 기본 생성
            return {
                "last_attendance": "",
                "streak": 0,
            }

        #읽기 모드
        with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    
    def _save(self) -> None:
        #쓰기 모드
        with open(ATTENDANCE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)



    #출석 처리
    def mark_attendance(self) -> bool:
    
        today = date.today()

        
        last_date_str = self.data["last_attendance"]

        if last_date_str:
            last_date = datetime.strptime(last_date_str,"%Y-%m-%d").date() #마지막 출석 날짜 가져옴

            diff = (today - last_date).days #날짜 차이 계산

            if diff == 0: #이미 출석
                return False

            if diff == 1: #연속출석
                self.data["streak"] += 1
            else: # 연속 출석 끊겼을때
                self.data["streak"] = 1

        else: #첫 출석
            self.data["streak"] = 1

        self.data["last_attendance"] = today.isoformat()


        self._save()
        return True

    def get_streak(self) -> int:
        return self.data["streak"]


    #오늘 출석 확인
    def is_attended_today(self) -> bool:
        return self.data["last_attendance"] == date.today().isoformat()