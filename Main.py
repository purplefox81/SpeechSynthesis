from xunfei.xunfei_api import SpeechSynthesis

# filename: the file name without extension
def run_me(filename):

    ssrh = SpeechSynthesis()
    with open('words/'+filename+'.txt') as file:

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

run_me("cn_p4a_6")
# run_me("en_p4a_6")
