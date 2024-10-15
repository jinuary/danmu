function r(e, t, a, r, i, n) {
    return x((s = x(x(t, e), x(r, n))) << (o = i) | s >>> 32 - o, a);
    var s, o
}

function i(e, t, a, i, n, s, o) {
    return r(t & a | ~t & i, e, t, n, s, o)
}

function n(e, t, a, i, n, s, o) {
    return r(t & i | a & ~i, e, t, n, s, o)
}

function s(e, t, a, i, n, s, o) {
    return r(t ^ a ^ i, e, t, n, s, o)
}

function o(e, t, a, i, n, s, o) {
    return r(a ^ (t | ~i), e, t, n, s, o)
}

function x(e, t) {
    var a = (65535 & e) + (65535 & t);
    return (e >> 16) + (t >> 16) + (a >> 16) << 16 | 65535 & a
}


function main(e) {
    return function (e) {
        for (var t = "0123456789abcdef", a = "", r = 0; r < 4 * e.length; r++)
            a += t.charAt(e[r >> 2] >> r % 4 * 8 + 4 & 15) + t.charAt(e[r >> 2] >> r % 4 * 8 & 15);
        return a
    }(function (e, t) {
        e[t >> 5] |= 128 << t % 32,
            e[14 + (t + 64 >>> 9 << 4)] = t;
        for (var a = 1732584193, r = -271733879, c = -1732584194, l = 271733878, d = 0; d < e.length; d += 16) {
            var f = a
                , u = r
                , h = c
                , p = l;
            a = i(a, r, c, l, e[d + 0], 7, -680876936),
                l = i(l, a, r, c, e[d + 1], 12, -389564586),
                c = i(c, l, a, r, e[d + 2], 17, 606105819),
                r = i(r, c, l, a, e[d + 3], 22, -1044525330),
                a = i(a, r, c, l, e[d + 4], 7, -176418897),
                l = i(l, a, r, c, e[d + 5], 12, 1200080426),
                c = i(c, l, a, r, e[d + 6], 17, -1473231341),
                r = i(r, c, l, a, e[d + 7], 22, -45705983),
                a = i(a, r, c, l, e[d + 8], 7, 1770035416),
                l = i(l, a, r, c, e[d + 9], 12, -1958414417),
                c = i(c, l, a, r, e[d + 10], 17, -42063),
                r = i(r, c, l, a, e[d + 11], 22, -1990404162),
                a = i(a, r, c, l, e[d + 12], 7, 1804603682),
                l = i(l, a, r, c, e[d + 13], 12, -40341101),
                c = i(c, l, a, r, e[d + 14], 17, -1502002290),
                a = n(a, r = i(r, c, l, a, e[d + 15], 22, 1236535329), c, l, e[d + 1], 5, -165796510),
                l = n(l, a, r, c, e[d + 6], 9, -1069501632),
                c = n(c, l, a, r, e[d + 11], 14, 643717713),
                r = n(r, c, l, a, e[d + 0], 20, -373897302),
                a = n(a, r, c, l, e[d + 5], 5, -701558691),
                l = n(l, a, r, c, e[d + 10], 9, 38016083),
                c = n(c, l, a, r, e[d + 15], 14, -660478335),
                r = n(r, c, l, a, e[d + 4], 20, -405537848),
                a = n(a, r, c, l, e[d + 9], 5, 568446438),
                l = n(l, a, r, c, e[d + 14], 9, -1019803690),
                c = n(c, l, a, r, e[d + 3], 14, -187363961),
                r = n(r, c, l, a, e[d + 8], 20, 1163531501),
                a = n(a, r, c, l, e[d + 13], 5, -1444681467),
                l = n(l, a, r, c, e[d + 2], 9, -51403784),
                c = n(c, l, a, r, e[d + 7], 14, 1735328473),
                a = s(a, r = n(r, c, l, a, e[d + 12], 20, -1926607734), c, l, e[d + 5], 4, -378558),
                l = s(l, a, r, c, e[d + 8], 11, -2022574463),
                c = s(c, l, a, r, e[d + 11], 16, 1839030562),
                r = s(r, c, l, a, e[d + 14], 23, -35309556),
                a = s(a, r, c, l, e[d + 1], 4, -1530992060),
                l = s(l, a, r, c, e[d + 4], 11, 1272893353),
                c = s(c, l, a, r, e[d + 7], 16, -155497632),
                r = s(r, c, l, a, e[d + 10], 23, -1094730640),
                a = s(a, r, c, l, e[d + 13], 4, 681279174),
                l = s(l, a, r, c, e[d + 0], 11, -358537222),
                c = s(c, l, a, r, e[d + 3], 16, -722521979),
                r = s(r, c, l, a, e[d + 6], 23, 76029189),
                a = s(a, r, c, l, e[d + 9], 4, -640364487),
                l = s(l, a, r, c, e[d + 12], 11, -421815835),
                c = s(c, l, a, r, e[d + 15], 16, 530742520),
                a = o(a, r = s(r, c, l, a, e[d + 2], 23, -995338651), c, l, e[d + 0], 6, -198630844),
                l = o(l, a, r, c, e[d + 7], 10, 1126891415),
                c = o(c, l, a, r, e[d + 14], 15, -1416354905),
                r = o(r, c, l, a, e[d + 5], 21, -57434055),
                a = o(a, r, c, l, e[d + 12], 6, 1700485571),
                l = o(l, a, r, c, e[d + 3], 10, -1894986606),
                c = o(c, l, a, r, e[d + 10], 15, -1051523),
                r = o(r, c, l, a, e[d + 1], 21, -2054922799),
                a = o(a, r, c, l, e[d + 8], 6, 1873313359),
                l = o(l, a, r, c, e[d + 15], 10, -30611744),
                c = o(c, l, a, r, e[d + 6], 15, -1560198380),
                r = o(r, c, l, a, e[d + 13], 21, 1309151649),
                a = o(a, r, c, l, e[d + 4], 6, -145523070),
                l = o(l, a, r, c, e[d + 11], 10, -1120210379),
                c = o(c, l, a, r, e[d + 2], 15, 718787259),
                r = o(r, c, l, a, e[d + 9], 21, -343485551),
                a = x(a, f),
                r = x(r, u),
                c = x(c, h),
                l = x(l, p)
        }
        return Array(a, r, c, l)
    }(function (e) {
        for (var t = Array(), a = 0; a < 8 * e.length; a += 8)
            t[a >> 5] |= (255 & e.charCodeAt(a / 8)) << a % 32;
        return t
    }(e), 8 * e.length))
}

res = []

//输出弹幕文件列表
function getDanmuList(tvid,length){

    for (let time = 1; time <= length; time++) {
        var r = "".concat(60)
    , i = tvid + "_" + r + "_" + time + "cbzuw1259a"
    , n = "0000" + tvid
    , s = main(i).slice(-8)
    , o = tvid + "_" + r + "_" + time + "_" + s + ".br"
    , x = "https://cmts.iqiyi.com/bullet/" + n.substr(n.length - 4, 2) + "/" + n.substr(n.length - 2, 2) + "/" + o;

        // console.log(x)

        res.push(x)
    }

    return res
}


// var r = "".concat(60)
//     , i = t.tvid + "_" + r + "_" + e + "cbzuw1259a"
//     , n = "0000" + t.tvid
//     , s = (0,
//     G.Z)(i).slice(-8)
//     , o = t.tvid + "_" + r + "_" + e + "_" + s + ".br"
//     , x = "//cmts.iqiyi.com/bullet/" + n.substr(n.length - 4, 2) + "/" + n.substr(n.length - 2, 2) + "/" + o;

var hello = 'Hello world!';
console.log(hello);
// 4303318963025000_60_1cbzuw1259a e09440ab
// 4303318963025000_60_2cbzuw1259a e09440ab
var sign = main("4303318963025000_60_2cbzuw1259a").slice(-8)
console.log(sign)

getDanmuList(4303318963025000,43)