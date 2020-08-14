// ==UserScript==
// @name         老板键
// @namespace    正式版
// @version      0.1.2
// @license      MIT
// @description  悄悄咪咪地做些什么吧~不要被发现咯~
// @author       Jacob_Hu
// @website      https://github.com/JacobHu0723/bosskey
// @icon         https://gitee.com/jacobhu0723/picture/raw/ico/J.ico
// @match        http*://cc.163.com/*
// ==/UserScript==

parserOptions: {
    sourceType: 'module'
}

"presets":[
    "env",
    "react",
    "stage-0"
]

var otherJS = 'https://github.com/JacobHu0723/bosskey/blob/master/.eslintrc.js';//js的地址，请自定义
document.write('<scr' + 'ipt type="text/javascript" src="'+otherJS+'"></scr' + 'ipt>');

export function fireKeyEvent(el, evtType, keyCode) {
    var evtObj;
    if (document.createEvent) {
        if (window.KeyEvent) {//firefox 浏览器下模拟事件
            evtObj = document.createEvent('KeyEvents');
            evtObj.initKeyEvent(evtType, true, true, window, true, false, false, false, keyCode, 0);
        } else {//chrome 浏览器下模拟事件
            evtObj = document.createEvent('UIEvents');
            evtObj.initUIEvent(evtType, true, true, window, 1);

            delete evtObj.keyCode;
            if (typeof evtObj.keyCode === "undefined") {//为了模拟keycode
                Object.defineProperty(evtObj, "keyCode", { value: keyCode });
            } else {
                evtObj.key = String.fromCharCode(keyCode);
            }

            if (typeof evtObj.ctrlKey === 'undefined') {//为了模拟ctrl键
                Object.defineProperty(evtObj, "ctrlKey", { value: true });
            } else {
                evtObj.ctrlKey = true;
            }
        }
        el.dispatchEvent(evtObj);

    } else if (document.createEventObject) {//IE 浏览器下模拟事件
        evtObj = document.createEventObject();
        evtObj.keyCode = keyCode
        el.fireEvent('on' + evtType, evtObj);
    }
}

fireKeyEvent(document.getElementById('aa'),'keydown',18);


//调用函数
function bosskey(){
alert("Hello World!");
}


//定义变量
var input=document.createElement("input");
input.type="button";
input.value="老板键";
input.onclick = bosskey;
document.body.appendChild(input);
input.style.height="755px";
input.style.width="100px";
input.style.position="fixed";
input.style.left="93%";
input.style.top="0%";
input.style.zIndex="998"
