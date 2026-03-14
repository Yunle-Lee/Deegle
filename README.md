![Deegle](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/46E6D3CE80742C3493AE0EA474DB6E10.jpg)
# Deegle 
**Deegle** 是一款集成网页搜索、PDF 预览与 DeepSeek AI 聊天的桌面应用，提供智能搜索、AI 对话、进度血条和用户等级系统，让你的信息检索和日常问答体验更智能、有趣。

---
## 展示：
1.输入deepseek api key<br>
![1](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-03-14%20181449.png)<br>
2.整个控制面板就长这个样子了<br>
![2](https://github.com/Yunle-Lee/Pics_of_all_my-projects/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202026-03-14%20180810.png)<br>

## 🌟 功能特点

### 1. 搜索功能
- 支持网页搜索和本地 PDF 文件搜索
- 搜索关键字在中央预览框高亮显示
- 搜索模板按钮快捷输入：
  - Github
  - Nvidia
  - 高木同学
  - Huggingface
  - 天气预报
- 搜索结果可在默认浏览器打开
- PDF 搜索会弹出文件选择框，直接预览和打开 PDF

### 2. AI 聊天（DeepSeek）
- 接入 DeepSeek API，实现多轮对话
- AI 知道自己的身份：**御小灵 (Aethelm)**，并知道开发者信息
- 蓝色流式显示 AI 回复
- 聊天支持上下文记忆
- 支持网络异常处理，提示用户而不崩溃

### 3. 用户进度系统
- 左下角显示 AI 形象
- **等级血条 Lv0~Lv9**，随使用次数增加
- **Token 使用血条**，显示 DeepSeek API 调用量
- 每个血条旁显示数字，让使用进度直观可见

### 4. 界面特点
- 三栏自适应布局（历史记录 / 搜索预览 / AI 聊天）
- 搜索和聊天历史显示时间记录
- 支持窗口大小调整，控件自动适配

---

## 🖥️ 安装与运行

### 1. 克隆项目
```bash
git clone https://github.com/Yunle-Lee/Deegle.git
cd Deegle
