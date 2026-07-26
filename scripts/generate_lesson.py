#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史课程交互式网页生成器

功能：
1. 读取结构化JSON数据
2. 生成包含转盘点名、时间线、图片展示的交互式HTML网页
3. 应用棕色系样式和古旧纸张背景
"""

import json
import sys
import os
import argparse
import random


def generate_html(json_data, student_list=None):
    """
    根据JSON数据生成交互式HTML网页
    
    Args:
        json_data: 包含网页内容的字典
        student_list: 学生名单列表（可选）
    
    Returns:
        HTML字符串
    """
    title = json_data.get('title', '历史课程')
    subtitle = json_data.get('subtitle', '')
    sections = json_data.get('sections', [])
    timeline = json_data.get('timeline', [])
    fun_facts = json_data.get('fun_facts', [])
    extra_resources = json_data.get('extra_resources', [])
    summary = json_data.get('summary', '')
    
    # 原版学生名单（固定）
    if student_list is None:
        student_list = [
            '张宇轩', '李思涵', '王浩然', '陈雨桐', '刘子墨',
            '赵一诺', '周嘉诚', '孙婉清', '黄梓涵', '林俊熙',
            '徐可欣', '郭晨阳', '马语彤', '何沐辰', '高欣怡',
            '唐子睿', '宋依然', '郑博文', '韩若曦', '蔡承泽'
        ]
    
    # 生成引入区HTML
    intro_html = ''
    for section in sections:
        if section.get('type') == 'intro':
            intro_html = f'''
        <!-- 引入区 -->
        <div class="section">
            <h2>一、引入：{section.get('title', '')}</h2>
            <div class="story-content">
'''
            for line in section.get('content', '').split('\n'):
                if line.strip():
                    intro_html += f'                <p>{line}</p>\n'
            
            # 添加图片（如果有）
            if section.get('image_url'):
                intro_html += f'''
            </div>
            
            <div class="image-container">
                <img src="{section.get('image_url')}" alt="{section.get('image_caption', '')}">
                <p>{section.get('image_caption', '')}</p>
            </div>
        </div>
'''
            else:
                intro_html += '''            </div>
        </div>
'''
            break
    
    # 生成时间线HTML
    timeline_html = ''
    if timeline:
        timeline_html = '''
        <!-- 时间线梳理 -->
        <div class="section">
            <h2>二、时间线梳理：{title}的发展脉络</h2>
            <div class="timeline">
'''.format(title=title)
        
        for i, event in enumerate(timeline):
            position = 'timeline-left' if i % 2 == 0 else 'timeline-right'
            timeline_html += f'''
                <div class="timeline-item {position}">
                    <div class="timeline-content">
                        <h4>{event.get('year', '')}</h4>
                        <p>{event.get('event', '')}</p>
                    </div>
                </div>
'''
        
        timeline_html += '''
            </div>
        </div>
'''
    
    # 生成知识点展开区HTML
    knowledge_html = '''
        <!-- 展开区 -->
        <div class="section">
            <h2>三、展开：{title}的核心知识点</h2>
'''.format(title=title)
    
    knowledge_count = 1
    for section in sections:
        if section.get('type') == 'knowledge':
            question = section.get('question', {})
            knowledge_html += f'''
            <div class="knowledge-point">
                <h3>知识点{knowledge_count}：{section.get('title', '')}</h3>
                <div class="story-content">
'''
            for line in section.get('content', '').split('\n'):
                if line.strip():
                    knowledge_html += f'                    <p>{line}</p>\n'
            
            knowledge_html += '''                </div>
'''
            
            # 添加图片
            if section.get('image_url'):
                knowledge_html += f'''
                <div class="image-container">
                    <img src="{section.get('image_url')}" alt="{section.get('image_caption', '')}">
                    <p>{section.get('image_caption', '')}</p>
                </div>
'''
            
            # 添加互动题目
            if question:
                question_type = question.get('type', 'thinking')  # 'thinking' or 'choice'
                question_text = question.get('text', '')
                hints = question.get('hints', [])
                answer = question.get('answer', '')
                options = question.get('options', [])
                
                question_title = '互动思考题' if question_type == 'thinking' else '互动选择题'
                
                knowledge_html += f'''
                <div class="interactive-question">
                    <h4>{question_title}</h4>
                    <div class="question-text">
                        {question_text}
                    </div>
'''
                
                # 如果是选择题，添加选项
                if question_type == 'choice' and options:
                    knowledge_html += '''                    <div class="options">
'''
                    for i, option in enumerate(options):
                        knowledge_html += f'''                        <div class="option">
                            <input type="radio" name="q{knowledge_count}" value="{chr(65+i)}">
                            <label>{chr(65+i)}. {option}</label>
                        </div>
'''
                    knowledge_html += '''                    </div>
'''
                
                # 添加提示按钮
                for i, hint in enumerate(hints):
                    knowledge_html += f'''                    <button class="hint-button" onclick="showHint('hint{knowledge_count}-{i+1}')">提示{i+1}</button>
'''
                
                knowledge_html += f'''                    <button class="answer-button" onclick="showAnswer('answer{knowledge_count}')">显示答案/解析</button>
'''
                
                # 添加提示内容
                for i, hint in enumerate(hints):
                    knowledge_html += f'''                    <div class="hint" id="hint{knowledge_count}-{i+1}">
                        <p>提示{i+1}：{hint}</p>
                    </div>
'''
                
                # 添加答案
                knowledge_html += f'''                    <div class="answer" id="answer{knowledge_count}">
                        <p>答案/解析：{answer}</p>
                    </div>
                </div>
'''
            
            knowledge_html += '''            </div>
'''
            knowledge_count += 1
    
    knowledge_html += '''        </div>
'''
    
    # 生成趣味补充HTML
    fun_facts_html = ''
    if fun_facts:
        fun_facts_html = '''
        <!-- 趣味补充 -->
        <div class="section">
            <h2>四、趣味补充：{title}的小知识</h2>
'''.format(title=title)
        
        for fact in fun_facts:
            fun_facts_html += f'''
            <div class="fun-fact">
                <h4>{fact.get('title', '')}</h4>
                <p>{fact.get('content', '')}</p>
            </div>
'''
        
        fun_facts_html += '''        </div>
'''
    
    # 生成课外兴趣资料HTML
    extra_html = ''
    if extra_resources:
        extra_html = '''
        <!-- 课外兴趣资料 -->
        <div class="section">
            <h2>五、课外兴趣资料</h2>
'''
        
        for resource in extra_resources:
            extra_html += f'''
            <div class="extra-resources">
                <h4>{resource.get('title', '')}</h4>
                <ul>
'''
            for item in resource.get('items', []):
                extra_html += f'                    <li>{item}</li>\n'
            
            extra_html += '''                </ul>
            </div>
'''
        
        extra_html += '''        </div>
'''
    
    # 生成完整HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>秋老师历史小课堂 - {title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'SimHei', 'Microsoft YaHei', sans-serif;
            background-color: #f0e6d6;
            color: #333;
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScyMjAnIGhlaWdodD0nMjIwJz48ZmlsdGVyIGlkPSduJz48ZmVUdXJidWxlbmNlIHR5cGU9J2ZyYWN0YWxOb2lzZScgYmFzZUZyZXF1ZW5jeT0nMC45JyBudW1PY3RhdmVzPScyJyBzdGl0Y2hUaWxlcz0nc3RpdGNoJy8+PGZlQ29sb3JNYXRyaXggdHlwZT0nc2F0dXJhdGUnIHZhbHVlcz0nMCcvPjxmZUNvbXBvbmVudFRyYW5zZmVyPjxmZUZ1bmNBIHR5cGU9J2xpbmVhcicgc2xvcGU9JzAuMDUnLz48L2ZlQ29tcG9uZW50VHJhbnNmZXI+PC9maWx0ZXI+PHJlY3Qgd2lkdGg9JzIyMCcgaGVpZ2h0PScyMjAnIGZpbGw9JyNlOWQ4YjAnLz48cmVjdCB3aWR0aD0nMjIwJyBoZWlnaHQ9JzIyMCcgZmlsdGVyPSd1cmwoI24pJy8+PC9zdmc+");  /* 内联羊皮纸纹理，离线可用 */
            background-repeat: repeat;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        h1 {{
            text-align: center;
            color: #8b4513;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            border-bottom: 3px solid #8b4513;
            padding-bottom: 10px;
        }}

        .section {{
            background-color: #fff8e7;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border: 2px solid #d4a066;
        }}

        .section h2 {{
            color: #8b4513;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #d4a066;
            padding-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }}

        .section h3 {{
            color: #8b4513;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.4em;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        }}

        .story-content {{
            font-size: 1.1em;
            line-height: 1.8;
            margin-bottom: 20px;
            color: #4d3319;
        }}

        .image-container {{
            text-align: center;
            margin: 25px 0;
        }}

        .image-container img {{
            max-width: 70%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 3px solid #d4a066;
        }}

        .image-container p {{
            margin-top: 10px;
            font-style: italic;
            color: #7f5539;
        }}

        .interactive-question {{
            background-color: #f5deb3;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            border: 2px solid #d4a066;
        }}

        .interactive-question h4 {{
            margin-bottom: 15px;
            color: #8b4513;
        }}

        .question-text {{
            font-size: 1.1em;
            margin-bottom: 20px;
            color: #4d3319;
        }}

        .options {{
            margin-bottom: 20px;
        }}

        .option {{
            margin-bottom: 12px;
            cursor: pointer;
            padding: 10px;
            border-radius: 5px;
            transition: background-color 0.3s ease;
            background-color: #fff8e7;
            border: 1px solid #d4a066;
        }}

        .option:hover {{
            background-color: #f0e6d6;
        }}

        .option input {{
            margin-right: 10px;
        }}

        .hint-button, .answer-button {{
            background-color: #8b4513;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 10px;
            font-size: 1em;
            transition: background-color 0.3s ease;
        }}

        .hint-button:hover, .answer-button:hover {{
            background-color: #654321;
        }}

        .hint, .answer {{
            margin-top: 15px;
            padding: 15px;
            border-radius: 5px;
            display: none;
        }}

        .hint {{
            background-color: #fff8e7;
            border: 1px solid #d4a066;
            color: #8b4513;
        }}

        .answer {{
            background-color: #fff8e7;
            border: 1px solid #d4a066;
            color: #8b4513;
        }}

        .progress-container {{
            margin: 25px 0;
        }}

        .progress-bar {{
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            border: 2px solid #d4a066;
        }}

        .progress-fill {{
            height: 100%;
            background-color: #8b4513;
            width: 0%;
            transition: width 0.5s ease;
        }}

        #progress-text {{
            text-align: center;
            margin-top: 10px;
            color: #8b4513;
            font-weight: bold;
        }}

        .achievement {{
            background-color: #fff8e7;
            border-left: 5px solid #8b4513;
            padding: 15px;
            margin: 20px 0;
            display: none;
            border: 2px solid #d4a066;
        }}

        .achievement h3 {{
            color: #8b4513;
            margin-bottom: 10px;
        }}

        .lucky-wheel {{
            text-align: center;
            margin: 30px 0;
        }}

        .wheel-container {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 0 auto 20px;
        }}

        .wheel {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(
                #ff6b6b 0deg 36deg,
                #4ecdc4 36deg 72deg,
                #45b7d1 72deg 108deg,
                #96ceb4 108deg 144deg,
                #ffeaa7 144deg 180deg,
                #dfe6e9 180deg 216deg,
                #b2bec3 216deg 252deg,
                #636e72 252deg 288deg,
                #2d3436 288deg 324deg,
                #0984e3 324deg 360deg
            );
            transition: transform 5s ease-out;
            border: 5px solid #8b4513;
        }}

        .wheel-pointer {{
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 15px solid transparent;
            border-right: 15px solid transparent;
            border-top: 30px solid #8b4513;
        }}

        .wheel-btn {{
            background-color: #8b4513;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
            font-size: 1.1em;
            transition: background-color 0.3s ease;
        }}

        .wheel-btn:hover {{
            background-color: #654321;
        }}

        .student-name {{
            font-size: 1.5em;
            font-weight: bold;
            color: #8b4513;
            margin: 20px 0;
        }}

        .sound-toggle {{
            text-align: center;
            margin: 20px 0;
        }}

        .sound-toggle button {{
            background-color: #8b4513;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        .sound-toggle button:hover {{
            background-color: #654321;
        }}

        .timeline {{
            position: relative;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px 0;
        }}

        .timeline::after {{
            content: '';
            position: absolute;
            width: 6px;
            background-color: #8b4513;
            top: 0;
            bottom: 0;
            left: 50%;
            margin-left: -3px;
        }}

        .timeline-item {{
            padding: 10px 40px;
            position: relative;
            background-color: inherit;
            width: 50%;
        }}

        .timeline-item::after {{
            content: '';
            position: absolute;
            width: 25px;
            height: 25px;
            right: -17px;
            background-color: #fff8e7;
            border: 4px solid #8b4513;
            top: 15px;
            border-radius: 50%;
            z-index: 1;
        }}

        .timeline-left {{
            left: 0;
        }}

        .timeline-right {{
            left: 50%;
        }}

        .timeline-left::before {{
            content: " ";
            height: 0;
            position: absolute;
            top: 22px;
            width: 0;
            z-index: 1;
            right: 30px;
            border: medium solid #fff8e7;
            border-width: 10px 0 10px 10px;
            border-color: transparent transparent transparent #fff8e7;
        }}

        .timeline-right::before {{
            content: " ";
            height: 0;
            position: absolute;
            top: 22px;
            width: 0;
            z-index: 1;
            left: 30px;
            border: medium solid #fff8e7;
            border-width: 10px 10px 10px 0;
            border-color: transparent #fff8e7 transparent transparent;
        }}

        .timeline-right::after {{
            left: -16px;
        }}

        .timeline-content {{
            padding: 20px 30px;
            background-color: #fff8e7;
            position: relative;
            border-radius: 6px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border: 2px solid #d4a066;
        }}

        .timeline-content h4 {{
            margin-top: 0;
            color: #8b4513;
        }}

        .fun-fact {{
            background-color: #fff8e7;
            border-left: 5px solid #8b4513;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            border: 2px solid #d4a066;
        }}

        .fun-fact h4 {{
            margin-top: 0;
            color: #8b4513;
        }}

        .extra-resources {{
            background-color: #fff8e7;
            border-left: 5px solid #8b4513;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            border: 2px solid #d4a066;
        }}

        .extra-resources h4 {{
            margin-top: 0;
            color: #8b4513;
        }}

        .extra-resources ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}

        .extra-resources li {{
            margin-bottom: 8px;
            color: #4d3319;
        }}

        @media screen and (max-width: 768px) {{
            h1 {{
                font-size: 2em;
            }}

            .section {{
                padding: 20px;
            }}

            .wheel-container {{
                width: 250px;
                height: 250px;
            }}

            .timeline::after {{
                left: 31px;
            }}

            .timeline-item {{
                width: 100%;
                padding-left: 70px;
                padding-right: 25px;
            }}

            .timeline-item::before {{
                left: 60px;
                border: medium solid #fff8e7;
                border-width: 10px 10px 10px 0;
                border-color: transparent #fff8e7 transparent transparent;
            }}

            .timeline-left::after, .timeline-right::after {{
                left: 15px;
            }}

            .timeline-right {{
                left: 0%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>秋老师历史小课堂</h1>
        <div class="subtitle" style="text-align: center; color: #8b4513; margin-bottom: 30px; font-size: 1.3em; font-style: italic;">{subtitle}</div>
        
        <div class="sound-toggle">
            <button id="sound-btn">音效开关</button>
        </div>

        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill"></div>
            </div>
            <p id="progress-text">进度：0%</p>
        </div>

        <div class="achievement" id="achievement">
            <h3>🎉 恭喜！解锁新成就</h3>
            <p>你已经完成了第一个知识点的学习，继续加油！</p>
        </div>

{intro_html}
{timeline_html}
{knowledge_html}
{fun_facts_html}
{extra_html}
        <!-- 互动区 -->
        <div class="section">
            <h2>六、互动：幸运点名转盘</h2>
            <div class="lucky-wheel">
                <div class="wheel-container">
                    <div class="wheel" id="wheel"></div>
                    <div class="wheel-pointer"></div>
                </div>
                <button class="wheel-btn" onclick="spinWheel()">开始抽奖</button>
                <button class="wheel-btn" onclick="spinWheel()">再抽一次</button>
                <div class="student-name" id="student-name"></div>
                <button class="wheel-btn" onclick="assignQuestion()">为TA出题</button>
            </div>
        </div>

        <!-- 总结区 -->
        <div class="section">
            <h2>七、总结：{title}的历史意义</h2>
            <div class="story-content">
                <p>{summary}</p>
            </div>

            <div class="interactive-question">
                <h4>开放题</h4>
                <div class="question-text">
                    请用自己的话解释本节课的核心命题
                </div>
            </div>
        </div>
    </div>

    <script>
        // 学生名单
        const students = {json.dumps(student_list, ensure_ascii=False)};

        // 进度跟踪
        let progress = 0;

        // 显示提示
        function showHint(hintId) {{
            const hint = document.getElementById(hintId);
            hint.style.display = 'block';
        }}

        // 显示答案
        function showAnswer(answerId) {{
            const answer = document.getElementById(answerId);
            answer.style.display = 'block';
            updateProgress(25); // 每次完成一个问题，进度增加25%
        }}

        // 更新进度
        function updateProgress(amount) {{
            progress += amount;
            if (progress > 100) progress = 100;
            const progressFill = document.getElementById('progress-fill');
            const progressText = document.getElementById('progress-text');
            progressFill.style.width = progress + '%';
            progressText.textContent = '进度：' + progress + '%';

            // 显示成就
            if (progress >= 50) {{
                document.getElementById('achievement').style.display = 'block';
            }}
        }}

        // 幸运点名转盘
        function spinWheel() {{
            const wheel = document.getElementById('wheel');
            const studentName = document.getElementById('student-name');
            const randomIndex = Math.floor(Math.random() * students.length);
            const selectedStudent = students[randomIndex];

            // 旋转转盘
            const rotation = 3600 + randomIndex * (360 / students.length);
            wheel.style.transform = 'rotate(' + rotation + 'deg)';

            // 显示结果
            setTimeout(() => {{
                studentName.textContent = '恭喜：' + selectedStudent;
            }}, 5000);
        }}

        // 为学生出题
        function assignQuestion() {{
            const studentName = document.getElementById('student-name').textContent;
            if (studentName) {{
                alert(studentName + '，请回答以下问题：{title}的主要特点是什么？');
            }} else {{
                alert('请先抽奖，选择一名学生！');
            }}
        }}

        // 音效开关
        let soundEnabled = false;
        const soundBtn = document.getElementById('sound-btn');

        soundBtn.addEventListener('click', () => {{
            soundEnabled = !soundEnabled;
            soundBtn.textContent = soundEnabled ? '音效：开启' : '音效：关闭';
        }});
    </script>
</body>
</html>
'''
    
    return html


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='生成历史课程交互式网页')
    parser.add_argument('--json-file', required=True, help='JSON数据文件路径')
    parser.add_argument('--output', required=True, help='输出HTML文件路径')
    parser.add_argument('--students', help='学生名单（JSON数组字符串）', default=None)
    
    args = parser.parse_args()
    
    # 读取JSON文件
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到JSON文件 {args.json_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：JSON文件解析失败 - {e}", file=sys.stderr)
        sys.exit(1)
    
    # 解析学生名单
    student_list = None
    if args.students:
        try:
            student_list = json.loads(args.students)
        except json.JSONDecodeError:
            print("警告：学生名单格式错误，使用默认名单", file=sys.stderr)
    
    # 生成HTML
    html_content = generate_html(json_data, student_list)
    
    # 写入输出文件
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功：网页已生成到 {args.output}")


if __name__ == '__main__':
    main()
