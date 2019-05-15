# 有道云笔记Markdown文档转换为一般格式的Markdown

- 有道云笔记Markdown中inline公式的语法为\`$..$\`, 单行公式为：\`\`\`math...\`\`\`

- 一般的Markdown文档中inline公式语法为$..$, 单行公式为$$...$$

例如，将有道云笔记的文档发表到CSDN博客上，需要进行大量的修改，所以就有了这个脚本。

用法：

```shell
youdaoNoteMD2MD.py source.md destitation.md
```