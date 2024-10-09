"""
为每个安卓控件生成一个不重复的字符，主要是将节点转换为单个字符，便于计算字符编辑距离
仅考虑控件的class，这样相似度的判断仅基于控件，没有考虑 text，resource-id，content-desc 等信息
"""

class2char_list = {
    "android.app.ActionBar$Tab": 'a',

    "android.support.v4.view.ViewPager": 'b',
    "android.support.v4.widget.DrawerLayout": 'b',

    "android.support.v7.app.ActionBar$Tab": 'c',
    "android.support.v7.app.ActionBar$b": 'c',
    "android.support.v7.widget.LinearLayoutCompat": 'd',
    "android.support.v7.widget.RecyclerView": 'd',

    "android.view.View": 'e',
    "android.webkit.WebView": 'e',
    "android.widget.AdapterView": 'e',

    "android.widget.Button": 'h',
    "android.widget.CompoundButton": 'h',
    "android.widget.ImageButton": 'h',
    "android.widget.RadioButton": 'h',
    "android.widget.ToggleButton": 'h',

    "android.widget.CheckBox": 'i',
    "android.widget.DatePicker": 'j',
    "android.widget.EditText": 'k',
    "android.widget.ExpandableListView": 'l',
    "android.widget.Gallery": 'm',
    "android.widget.GridView": 'n',
    "android.widget.HorizontalScrollView": 'o',
    "android.widget.Image": 'p',
    "android.widget.ImageView": 'q',

    "android.widget.FrameLayout": 'r',
    "android.widget.LinearLayout": 'r',
    "android.widget.RelativeLayout": 'r',
    "android.widget.TableLayout": 'r',

    "android.widget.TextView": 's',
    "android.widget.MultiAutoCompleteTextView": 's',
    "android.widget.CheckedTextView": 's',

    "android.widget.ListView": 'A',
    "android.widget.NumberPicker": 'B',
    "android.widget.ProgressBar": 'C',
    "android.widget.RatingBar": 'D',
    "android.widget.ScrollView": 'E',
    "android.widget.SearchView": 'F',
    "android.widget.SeekBar": 'G',
    "android.widget.Spinner": 'H',
    "android.widget.Switch": 'I',
    "android.widget.TabHost": 'G',
    "android.widget.TabWidget": 'K',
    "android.widget.TimePicker": 'L',
    "android.widget.VideoView": 'M',
    "android.widget.ViewAnimator": 'N',
    "android.widget.ViewFlipper": 'O',
    "androidx.recyclerview.widget.RecyclerView": 'P',
    "androidx.viewpager.widget.ViewPager": 'Q',
    "com.android.inputmethod.keyboard.Key": 'R',
    "android.view.ViewGroup": 'S',
    "android.widget.TableRow": 'T',
    "TextInputLayout": 'U',

    "hierarchy": '0'
}


def path2string(path):
    """
    将路径中的非叶子节点的类映射成为一个char从而将path转化为字符串从而计算字符串编辑距离
    :param path: 一条从根节点到叶子节点的树的路径
    :return: 映射成为的字符串
    """
    str = ''
    for node in path:
        if node.get('class') in class2char_list:
            str += class2char_list[node.get('class')]
        else:
            str += 'Z'
    # 删除字符串中叶子节点对应的字符
    return str[: -1]


def class2char(str):
    if str in class2char_list:
        return class2char_list[str]
    else:
        return 'Z'

