import random
import time
import ipywidgets as widgets
from IPython.display import display, clear_output

# 주기율표 데이터베이스 (1~20번)
ELEMENTS_DB = {
    1: ["수소", "H", "H+"], 2: ["헬륨", "He", "없음"], 3: ["리튬", "Li", "Li+"], 4: ["베릴륨", "Be", "Be2+"],
    5: ["붕소", "B", "없음"], 6: ["탄소", "C", "없음"], 7: ["질소", "N", "N3-"], 8: ["산소", "O", "O2-"],
    9: ["플루오린", "F", "F-"], 10: ["네온", "Ne", "없음"], 11: ["나트륨", "Na", "Na+"], 12: ["마그네슘", "Mg", "Mg2+"],
    13: ["알루미늄", "Al", "Al3+"], 14: ["규소", "Si", "없음"], 15: ["인", "P", "P3-"], 16: ["황", "S", "S2-"],
    17: ["염소", "Cl", "Cl-"], 18: ["아르곤", "Ar", "없음"], 19: ["칼륨", "K", "K+"], 20: ["칼슘", "Ca", "Ca2+"]
}

# 상태 변수
score = 0
current_question = 0
total_questions = 20
current_correct_ans = ""
selected_mode = '1'
is_endless = False

# 위젯 설정
out = widgets.Output()

mode_select = widgets.Dropdown(
    options=[
        ('1. 원소 번호 ➡️ 원소 이름', '1'),
        ('2. 원소 기호 ➡️ 원소 번호', '2'),
        ('3. 원소 이름 ➡️ 주요 이온식', '3')
    ],
    value='1',
    description='학습 모드:'
)

count_select = widgets.Dropdown(
    options=[
        ('10문제', 10),
        ('20문제', 20),
        ('50문제', 50),
        ('100문제', 100),
        ('무제한 (언제든 종료)', -1)
    ],
    value=20,
    description='문제 수:'
)

start_button = widgets.Button(description="퀴즈 시작 🚀", button_style='primary')
stop_button = widgets.Button(description="학습 종료 및 결과 보기 🏁", button_style='danger')

choice_buttons = [widgets.Button(layout=widgets.Layout(width='280px', height='45px')) for _ in range(4)]
button_box = widgets.VBox(choice_buttons)

def next_question():
    global current_question, current_correct_ans
    
    with out:
        clear_output()
        
        # 문제 수 도달 시 종료
        if not is_endless and current_question >= total_questions:
            finish_quiz()
            return

        current_question += 1
        target_num = random.randint(1, 20)
        info = ELEMENTS_DB[target_num]

        q_count_str = f"문제 {current_question}" if is_endless else f"문제 {current_question}/{total_questions}"

        if selected_mode == '1':
            print(f"[{q_count_str}] 원소 번호 {target_num}번의 이름은?\n")
            current_correct_ans = info[0]
            pool = [v[0] for v in ELEMENTS_DB.values()]
        elif selected_mode == '2':
            print(f"[{q_count_str}] 원소 기호 '{info[1]}'의 원소 번호는?\n")
            current_correct_ans = f"{target_num}번"
            pool = [f"{k}번" for k in ELEMENTS_DB.keys()]
        elif selected_mode == '3':
            print(f"[{q_count_str}] '{info[0]}({info[1]})'의 주요 이온식은?\n")
            current_correct_ans = info[2]
            pool = list(set([v[2] for v in ELEMENTS_DB.values()]))

        # 보기 생성 및 섞기
        wrongs = [opt for opt in pool if opt != current_correct_ans]
        choices = random.sample(wrongs, 3) + [current_correct_ans]
        random.shuffle(choices)

        # UI 출력 설정
        button_box.layout.display = 'block'
        stop_button.layout.display = 'block'
        
        colors = ['info', 'warning', 'success', 'primary']
        for btn, choice, col in zip(choice_buttons, choices, colors):
            btn.description = str(choice)
            btn.button_style = ''

def finish_quiz():
    button_box.layout.display = 'none'
    stop_button.layout.display = 'none'
    with out:
        clear_output()
        print("=" * 50)
        total_played = current_question - 1 if is_endless else total_questions
        if total_played > 0:
            rate = int((score / total_played) * 100)
            print(f"🎉 학습 완료! 최종 점수: {score} / {total_played} (정답률: {rate}%)")
        else:
            print("풀이한 문제가 없습니다.")
        print("=" * 50)

def on_choice_click(btn):
    global score
    with out:
        if btn.description == current_correct_ans:
            print("⭕ 정답입니다!")
            score += 1
        else:
            print(f"❌ 틀렸습니다! 정답은 [{current_correct_ans}] 입니다.")
    
    time.sleep(0.7)
    next_question()

def start_quiz(b):
    global score, current_question, selected_mode, total_questions, is_endless
    score = 0
    current_question = 0
    selected_mode = mode_select.value
    
    if count_select.value == -1:
        is_endless = True
    else:
        is_endless = False
        total_questions = count_select.value
        
    next_question()

def stop_quiz(b):
    finish_quiz()

# 이벤트 연결
start_button.on_click(start_quiz)
stop_button.on_click(stop_quiz)
for btn in choice_buttons:
    btn.on_click(on_choice_click)

# 화면 레이아웃 표시
display(widgets.HBox([mode_select, count_select]), start_button, out, button_box, stop_button)
button_box.layout.display = 'none'
stop_button.layout.display = 'none'
