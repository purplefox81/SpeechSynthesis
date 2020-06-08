from xunfei.xunfei_api import SpeechSynthesis

# filename: the file name without extension
def run_me(filename):

    ssrh = SpeechSynthesis()

    with open('words_primary/' + filename + '.txt') as file:

        chinese = filename.startswith('cn_')

        print('processing file ---',filename)
        lines = file.readlines()
        for i in range(len(lines)):
            my_text = lines[i].strip()
            print('processing',my_text)
            if chinese:
                my_final_text = '第' + str(i) + '句开始。' + my_text + '第' + str(i) + '句结束。'
                ssrh.synthesize(my_final_text,1)
            else:
                my_final_text = my_text
                ssrh.synthesize(my_final_text,50)
            ssrh.convert_to_mp3(filename+'_Line_'+str(i)+'.mp3')
    ssrh.clean_up()

# 已经重做
# run_me('cn_p1a_xie')
# run_me('cn_p1b_xie')
# run_me('cn_p2a_xie')
# run_me('cn_p2b_xie')
# run_me('cn_p3a_xie')
run_me('cn_p3b_xie')

# 等待重做
# run_me('cn_p2a_xie_1')
# run_me('cn_p2b_xie_1')
# run_me('cn_p2b_xie_2')
# run_me('cn_p3a_xie_1')
# run_me('cn_p3a_xie_2')
# run_me('cn_p3b_xie_1')
# run_me('cn_p3b_xie_2')


# 全部放弃
# run_me('cn_p1a_du_1')
# run_me('cn_p1a_du_2')
# run_me('cn_p1a_du_3')
# run_me('cn_p1b_du_1')
# run_me('cn_p1b_du_2')
# run_me('cn_p2a_du_1')
# run_me('cn_p2a_du_2')
# run_me('cn_p2b_du_1')
# run_me('cn_p2b_du_2')
# run_me('cn_p3a_du_1')
# run_me('cn_p3a_du_2')
# run_me('cn_p3a_du_3')
# run_me('cn_p3b_du_1')
# run_me('cn_p3b_du_2')

# 学校听写
# run_me("cn_p4a_tingxie_1")
# run_me("cn_p4a_tingxie_2")
# run_me("cn_p4a_tingxie_3")
# run_me("cn_p4a_tingxie_4")
# run_me("cn_p4a_tingxie_5")
# run_me("cn_p4a_tingxie_6")
# run_me("cn_p4a_tingxie_6")
# run_me("cn_p4a_tingxie_7")
# run_me("cn_p4a_tingxie_8")
# run_me("cn_p4a_tingxie_9")


