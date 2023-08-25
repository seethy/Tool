from manimlib import *
##
#  年龄问题:姐姐今年13岁，弟弟今年9岁，当姐弟俩岁数和是40岁时，两人各应该多少岁？
##

class AgeDiffer(Scene):
    def construct(self):
        txt_oldersister = Text("姐姐:", font="SimHei", font_size=25)
        dot_1left = Dot([-2, 0.5, 0])
        dot_1right = Dot([2, 0.5, 0])
        line1 = Line(dot_1left.get_center(), dot_1right.get_center()).set_color(ORANGE)
        b1 = Brace(line1, direction=UP)
        b1text = b1.get_text("13岁", font="SimHei", font_size=25)
        #b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        #b2text = b2.get_tex("x-x_1")
        txt_oldersister.shift([-3,0.5,0])
        #VGroup(line, txt_oldersister).arrange(direction=LEFT)
        self.add(txt_oldersister)
        self.play(Write(line1))
        self.add(dot_1left,dot_1right)
        self.play(Write(b1))
        self.add(b1text)
        vg1 = VGroup(line1,dot_1left,dot_1right,b1,b1text)

        txt_youngersister = Text("妹妹:", font="SimHei", font_size=25)
        dot_2left = Dot([-2, -0.5, 0])
        dot_2right = Dot([1, -0.5, 0])
        line2 = Line(dot_2left.get_center(), dot_2right.get_center()).set_color(ORANGE)
        b2 = Brace(line2, direction=DOWN)
        b2text = b2.get_text("9岁", font="SimHei", font_size=25)
        txt_youngersister.shift([-3, -0.5, 0])
        self.add(txt_youngersister)
        self.play(Write(line2))
        self.add(dot_2left, dot_2right)
        self.play(Write(b2))
        self.add(b2text)
        vg2 = VGroup(line2, dot_2left, dot_2right, b2, b2text)

        self.wait(2)
        ddot_1left = Dot([-2, 0.5, 0])
        ddot_1center = Dot([-1, 0.5, 0])
        dline1 = Line(ddot_1left.get_center(), ddot_1center.get_center()).set_color(BLUE)
        db1 = Brace(dline1, direction=UP)
        db1text = db1.get_text("n岁", font="SimHei", font_size=25)
        vg1.shift(RIGHT*1)
        self.play(Write(dline1))
        self.add(ddot_1left,ddot_1center)
        self.play(Write(db1))
        self.add(db1text)

        ddot_2left = Dot([-2, -0.5, 0])
        ddot_2center = Dot([-1, -0.5, 0])
        dline2 = Line(ddot_2left.get_center(), ddot_2center.get_center()).set_color(BLUE)
        db2 = Brace(dline2, direction=DOWN)
        db2text = db2.get_text("n岁", font="SimHei", font_size=25)
        vg2.shift(RIGHT * 1)
        self.play(Write(dline2))
        self.add(ddot_2left, ddot_2center)
        self.play(Write(db2))
        self.add(db2text)

        b_dot1 = Dot([3.5, 0.5, 0])
        b_dot2 = Dot([3.5, -0.5, 0])
        b_line = Line(b_dot1.get_center(), b_dot2.get_center())
        bracetotal = Brace(b_line, direction=RIGHT)
        bt_text = bracetotal.get_text("40岁", font="SimHei", font_size=25)
        self.play(Write(bracetotal))
        self.add(bt_text)

        self.wait(5)
        ddot_2center = Dot([2, -0.5, 0])
        ddot_2right = Dot([3, -0.5, 0])
        ddline2 = DashedLine(ddot_2center.get_center(), ddot_2right.get_center()).set_color(RED)
        ddb2 = Brace(ddline2, direction=DOWN)
        ddb2text = ddb2.get_text("差4岁", font="SimHei", font_size=25)
        self.play(Write(ddline2))
        self.add(ddot_2center, ddot_2right)
        self.play(Write(ddb2))
        self.add(ddb2text)









if __name__ == "__main__":
    from os import system
    configfile = "d:\cauchy\workspace\Tool\math\custom_config.yml"
    system("manimgl %s AgeDiffer -c BLACK --config_file %s" %(format(__file__), configfile))