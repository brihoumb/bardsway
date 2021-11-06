import logging

import sciter


last = list()
stream = None
percent = None
console = None
HTMLroot = None
started = False


def has_started(start=False):
    global started
    if start:
        started = start
    return started


def check_log_type(str, types):
    for type in types:
        if str.find(type) != -1:
            return 1
    return 0


def find_tags(str, types):
    for type in types:
        str = str.replace(type, '')
    return str


def init(root):
    global console, HTMLroot, stream

    HTMLroot = root
    console = logging.getLogger('').handlers[1]
    stream = console.stream


def reset():
    global HTMLroot, started, percent
    pathWav = HTMLroot.find_first('#pathWav')
    wavText = HTMLroot.find_first('#loadWav')
    launchText = HTMLroot.find_first('#launch')
    wavPic = HTMLroot.find_first('#loadWavPic')
    launchPic = HTMLroot.find_first('#launchPic')
    percent_element = HTMLroot.find_first('#progress-bar')

    wavText.set_style_attribute('color', '#43BCB5')
    launchText.set_style_attribute('color', '#2B2B2B')
    percent_element.set_style_attribute('width', '0%')
    pathWav.set_style_attribute('visibility', 'visible')
    wavPic.set_attribute('src', '../resources/file_b.svg')
    launchPic.set_attribute('src', '../resources/rocket_n.svg')

    percent = None
    started = False


def retrieve_log(root=None):
    global console, HTMLroot, last, stream, percent

    if root != HTMLroot:
        HTMLroot = root
    if console is None or stream is None:
        init(root)

    save = []
    if percent is None:
        if len(stream.getvalue().strip('\x00').split('\n')) > 1:
            save = stream.getvalue().strip('\x00').split('\n')[-6:-1]
        stream.seek(0)
        stream.truncate(0)

    logs = save + list(filter(None, stream.getvalue().strip('\x00').split('\n')))
    [spt, rdn, bsw] = HTMLroot.find_all('.out')

    percent_element = HTMLroot.find_first('#progress-bar')
    if percent is None:
        percent = int(percent_element.style_attribute('width')[:-1])

    bw_tags = ['---', '-=-', '-|-', '-+-']
    rdn_tags = ['-$-']

    for el in logs:
        if el not in last:
            if check_log_type(el, bw_tags):
                bsw.append(sciter.Element.create('p', find_tags(el, bw_tags)))
            elif check_log_type(el, rdn_tags):
                rdn.append(sciter.Element.create('p', find_tags(el, rdn_tags)))
                percent += 9
                percent_element.set_style_attribute('width', f'{percent}%')
            else:
                spt.append(sciter.Element.create('p', el))
                percent += 9
                percent_element.set_style_attribute('width', f'{percent}%')
            last.append(el)
        if el.find('PROGRAM OVER') != -1:
            reset()
