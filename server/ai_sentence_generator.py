from utils import generate_sentence, save_sentence

# 6時と18時に例文を生成
def schedule_example_generation():
    am_sentence = generate_sentence()
    pm_sentence = generate_sentence()
    
    save_sentence(am_sentence)
    save_sentence(pm_sentence)

if __name__ == '__main__':
    schedule_example_generation()
