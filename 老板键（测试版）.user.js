// ==UserScript==
// @name         老板键（测试版）
// @nameapace    测试版
// @version      0.2.2
// @license      MIT
// @description  悄悄咪咪地做些什么吧~不要被发现咯~
// @author       Jacob_Hu
// @website      https://github.com/JacobHu0723/bosskey
// @icon         https://gitee.com/jacobhu0723/picture/raw/ico/J.ico
// @include      http*://cc.163.com/*
// ==/UserScript==


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

//调用函数
function bosskey()
{
    function fireKeyEvent(el, evtType, keyCode) {
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

    var testPassword = "181818";
    var tp;
    var cCode;
    var testss = document.getElementById("input_txt_50531_740884");
    for(var i=0;i<testPassword.length;i++){
        cCode = testPassword.charCodeAt(i);
        fireKeyEvent(testss, "keydown", cCode);
        fireKeyEvent(testss, "keypress", cCode);
        fireKeyEvent(testss, "keyup", cCode);
    }
fireKeyEvent(document.getElementById('aa'),'keydown',18);
}
