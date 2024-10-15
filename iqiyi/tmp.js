// getBarrageBrData: function (e, t) {
//     var a = this;
//     a.isSetRequestTime || (a.isSetRequestTime = !0,
//         DANMU.firstSendRequestTime = +new Date),
//         a._ctrl.pingback.sendBlockPingback("pcw_total_barrage"),
//         function (e, t, a) {
//             var r = "".concat(60)
//                 , i = t.tvid + "_" + r + "_" + e + "cbzuw1259a"
//                 , n = "0000" + t.tvid
//                 , s = (0,
//                     G.Z)(i).slice(-8)
//                 , o = t.tvid + "_" + r + "_" + e + "_" + s + ".br"
//                 ,
//                 x = "//cmts.iqiyi.com/bullet/" + n.substr(n.length - 4, 2) + "/" + n.substr(n.length - 2, 2) + "/" + o;
//             (new E).load(x, (function (e, t) {
//                     if ("err" != e)
//                         try {
//                             if (200 == t.status) {
//                                 var r = e.response;
//                                 a(r)
//                             }
//                         } catch (e) {
//                         }
//                 }
//             ))
//         }(e, a.dataList, (function (r) {
//                 a.isSetResponseTime || (a.isSetResponseTime = !0,
//                     DANMU.firstSendResponseTime = +new Date),
//                     a._ctrl.pingback.sendBlockPingback("pcw_req_barrage"),
//                     a.complieDanmu(e, r, t)
//             }
//         ))
// }