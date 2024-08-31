
const NodeRSA = require('node-rsa');
const crypto = require('crypto');
const CryptoJS = require("crypto-js");


function ie(e) {
  this["$_JIT"] = e || [];
}

ie["prototype"] = {
  "$_FAE": function (e) {
  return this["$_JIT"][e];
  },
  "$_BAAy": function () {
  return this["$_JIT"]["length"];
  },
  "$_BBH": function (e, t) {
  return new ie(J(t) ? this["$_JIT"]["slice"](e, t) : this["$_JIT"]["slice"](e));
  },
  "$_BABR": function (e) {
  return this["$_JIT"]["push"](e), this;
  },
  "$_BACx": function (e, t) {
  return this["$_JIT"]["splice"](e, t || 1);
  },
  "$_BDh": function (e) {
  return this["$_JIT"]["join"](e);
  },
  "$_BADD": function (e) {
  return new ie(this["$_JIT"]["concat"](e));
  },
  "$_BCa": function (e) {
  var t = this["$_JIT"];
  if (t["map"]) return new ie(t["map"](e));
  for (var n = [], r = 0, i = t["length"]; r < i; r += 1) n[r] = e(t[r], r, this);
  return new ie(n);
  },
  "$_BAE_": function (e) {
  var t = this["$_JIT"];
  if (t["filter"]) return new ie(t["filter"](e));
  for (var n = [], r = 0, i = t["length"]; r < i; r += 1) e(t[r], r, this) && n["push"](t[r]);
  return new ie(n);
  },
  "$_BAFA": function (e) {
  var t = this["$_JIT"];
  if (t["indexOf"]) return t["indexOf"](e);
  for (var n = 0, r = t["length"]; n < r; n += 1) if (t[n] === e) return n;
  return -1;
  },
  "$_BAGB": function (e) {
  var t = this["$_JIT"];
  if (!t["forEach"]) for (var n = arguments[1], r = 0; r < t["length"]; r++) r in t && e["call"](n, t[r], r, this);
  return t["forEach"](e);
  }
}
ie["$_JHn"] = function (e) {
  return Array["isArray"] ? Array["isArray"](e) : "[object Array]" === Object["prototype"]["toString"]["call"](e);
}

pe = {
  "$_BFER":  300,
  "$_BFDn": function () {
  var r = this;
  r["$_BEGQ"]["$_JBG"]("move", function (e) {
      r["$_BFFQ"](), r["posX"] = e["$_BECm"](), r["posY"] = e["$_BEDf"](), r["$_BFGo"]("move", r["posX"], r["posY"], e["$_FBK"]["type"]);
  })["$_JBG"]("down", function (e) {
      var t = r["$_FC_"]["length"];
      r["$_FC_"][t - 1] && "down" === r["$_FC_"][t - 1][0] || (r["$_BFFQ"](), r["posX"] = e["$_BECm"](), r["posY"] = e["$_BEDf"](), r["$_BFGo"]("down", r["posX"], r["posY"], e["$_FBK"]["type"]), r["$_FC_"][t - 2] && "move" === r["$_FC_"][t - 2][0] && r["$_FC_"][t - 3] && "up" === r["$_FC_"][t - 3][0] && r["$_BFHA"](t - 2));
  })["$_JBG"]("up", function (e) {
      var t = r["$_FC_"]["length"];
      r["$_FC_"][t - 1] && "up" === r["$_FC_"][t - 1][0] || (r["$_BFFQ"](), r["posX"] = e["$_BECm"](), r["posY"] = e["$_BEDf"](), r["$_BFGo"]("up", r["posX"], r["posY"], e["$_FBK"]["type"]), r["$_FC_"][t - 2] && "move" === r["$_FC_"][t - 2][0] && r["$_FC_"][t - 3] && "down" === r["$_FC_"][t - 3][0] && r["$_BFHA"](t - 2));
  })["$_JBG"]("focusin", function () {
      r["$_BFGo"]("focus");
  }), r["$_BEHV"]["$_JBG"]("scroll", function () {
      var e = ("pageXOffset" in window),
      t = e ? window["pageXOffset"] : l["body"]["scrollLeft"],
      n = e ? window["pageYOffset"] : l["body"]["scrollTop"];
      r["posX"] = t - r["scrollLeft"] + r["posX"], r["posY"] = n - r["scrollTop"] + r["posY"], r["$_BFGo"]("scroll", t - r["scrollLeft"] + r["posX"], n - r["scrollTop"] + r["posY"]), r["$_BFFQ"]();
  })["$_JBG"]("focus", function () {
      r["$_BFGo"]("focus");
  })["$_JBG"]("blur", function () {
      r["$_BFGo"]("blur");
  })["$_JBG"]("unload", function () {
      r["$_BFGo"]("unload");
  });
  },
  "$_BFFQ": function () {
  var e = ("pageXOffset" in window),
      t = e ? window["pageXOffset"] : l["body"]["scrollLeft"],
      n = e ? window["pageYOffset"] : l["body"]["scrollTop"];
  return {
      "x": this["scrollLeft"] = t,
      "y": this["scrollTop"] = n
  };
  },
  "$_BFGo": function (e, t, n, r) {
  var i = $_FB(),
      s = this,
      o = s["$_BFAU"],
      _ = s["$_BFBP"],
      a = s["$_BFCl"],
      c = s["$_FC_"];
  if (-1 < new ie(["move", "down", "up", "scroll"])["$_BAFA"](e)) {
      if ("move" === e) {
      if (t === o && n === _ || a === i) return;
      s["$_BFAU"] = t, s["$_BFBP"] = n, s["$_BFCl"] = i;
      }
      c["push"]([e, s["$_BFIQ"](t), s["$_BFIQ"](n), i, r]);
  } else c["push"]([e, i]);
  return s;
  },
  "$_BFHA": function (e) {
  this["$_FC_"]["splice"](e, 1);
  },
  "$_JDi": function () {
  this["$_BEHV"]["$_BCGr"](), this["$_BEGQ"]["$_BCGr"]();
  },
  "$_BFJj": function (e) {
  var t = 0,
      n = 0,
      r = [],
      i = this,
      s = i["lastTime"];
  if (e["length"] <= 0) return [];
  for (var o = null, _ = null, a = i["$_BGAB"](e), c = a["length"], l = c < this["$_BFER"] ? 0 : c - this["$_BFER"]; l < c; l += 1) {
      var u = a[l],
      h = u[0];
      -1 < new ie(["down", "move", "up", "scroll"])["$_BAFA"](h) ? (o || (o = u), _ = u, r["push"]([h, [u[1] - t, u[2] - n], i["$_BFIQ"](s ? u[3] - s : s)]), t = u[1], n = u[2], s = u[3]) : -1 < new ie(["blur", "focus", "unload"])["$_BAFA"](h) && (r["push"]([h, i["$_BFIQ"](s ? u[1] - s : s)]), s = u[1]);
  }
  return i["$_BEIU"] = o, i["$_BEJu"] = _, r;
  },
  "$_BGAB": function (e) {
  var t = "",
      n = 0;
  (e || [])["length"];
  while (!t && e[n]) t = e[n] && e[n][4], n++;
  if (!t) return e;
  for (var r = "", i = ["mouse", "touch", "pointer", "MSPointer"], s = 0, o = i["length"]; s < o; s++) 0 === t["indexOf"](i[s]) && (r = i[s]);
  for (var _ = e["slice"](), a = _["length"] - 1; 0 <= a; a--) {
      var c = _[a],
      l = c[0];
      if (-1 < new ie(["move", "down", "up"])["$_BAFA"](l)) 0 !== (c[4] || "")["indexOf"](r) && _["splice"](a, 1);
  }
  return _;
  },
  "$_EEs": function (e) {
  var h = {
      "move": 0,
      "down": 1,
      "up": 2,
      "scroll": 3,
      "focus": 4,
      "blur": 5,
      "unload": 6,
      "unknown": 7
  };
  function p(e, t) {
      for (var n = e["toString"](2), r = "", i = n["length"] + 1; i <= t; i += 1) r += "0";
      return n = r + n;
  }
  var d = function (e) {
      var t = [],
      n = e["length"],
      r = 0;
      while (r < n) {
      var i = e[r],
          s = 0;
      while (1) {
          if (16 <= s) break;
          var o = r + s + 1;
          if (n <= o) break;
          if (e[o] !== i) break;
          s += 1;
      }
      r = r + 1 + s;
      var _ = h[i];
      0 != s ? (t["push"](8 | _), t["push"](s - 1)) : t["push"](_);
      }
      for (var a = p(32768 | n, 16), c = "", l = 0, u = t["length"]; l < u; l += 1) c += p(t[l], 4);
      return a + c;
  };
  function c(e, t) {
      for (var n = [], r = 0, i = e["length"]; r < i; r += 1) n["push"](t(e[r]));
      return n;
  }
  function g(e, t) {
  e = function a(e) {
  var t = 32767,
      n = (e = c(e, function (e) {
      return t < e ? t : e < -t ? -t : e;
      }))["length"],
      r = 0,
      i = [];
  while (r < n) {
      var s = 1,
      o = e[r],
      _ = Math["abs"](o);
      while (1) {
      if (n <= r + s) break;
      if (e[r + s] !== o) break;
      if (127 <= _ || 127 <= s) break;
      s += 1;
      }
      1 < s ? i["push"]((o < 0 ? 49152 : 32768) | s << 7 | _) : i["push"](o), r += s;
  }
  return i;
  }(e);
  var n,
  r = [],
  i = [];
  c(e, function (e) {
  var t = Math["ceil"](function n(e, t) {
      return 0 === e ? 0 : Math["log"](e) / Math["log"](t);
  }(Math["abs"](e) + 1, 16));
  0 === t && (t = 1), r["push"](p(t - 1, 2)), i["push"](p(Math["abs"](e), 4 * t));
  });
  var s = r["join"](""),
  o = i["join"]("");
  return n = t ? c(function _(e, t) {
  var n = [];
  return c(e, function (e) {
      t(e) && n["push"](e);
  }), n;
  }(e, function (e) {
  return 0 != e && e >> 15 != 1;
  }), function (e) {
  return e < 0 ? "1" : "0";
  })["join"]("") : "", p(32768 | e["length"], 16) + s + o + n;
}
return function (e) {
  for (var t = [], n = [], r = [], i = [], s = 0, o = e["length"]; s < o; s += 1) {
  var _ = e[s],
      a = _["length"];
  t["push"](_[0]), n["push"](2 === a ? _[1] : _[2]), 3 === a && (r["push"](_[1][0]), i["push"](_[1][1]));
  }
  var c = d(t) + g(n, !1) + g(r, !0) + g(i, !0),
  l = c["length"];
  return l % 6 != 0 && (c += p(0, 6 - l % 6)), function u(e) {
  for (var t = "", n = e["length"] / 6, r = 0; r < n; r += 1) t += "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~"["charAt"](parseInt(e["slice"](6 * r, 6 * (r + 1)), 2));
  return t;
  }(c);
}(e);
},
"$_BFIQ": function (e) {
var t = 32767;
return "number" != typeof e ? e : (t < e ? e = t : e < -t && (e = -t), Math["round"](e));
},
"$_BGBv": function () {
return this["$_EEs"](this["$_BFJj"](this["$_FC_"]))["length"];
},
"$_BGCW": function (e) {
return this["$_EEs"](this["$_BFJj"](e));
},
"$_BGDT": function () {
return this["$_EEs"](this["$_FC_"]);
}
}





geteee= function(numActions, num){
    const data = [];
    let prevX = 763; // 初始 x 坐标
    let prevY = 20;  // 初始 y 坐标
    let prevTimestamp = Date.now() - 3000; // 初始时间戳
    mmm = num;
    for (let i = 0; i < numActions; i++) {
        x = prevX + Math.floor(Math.random() * 10) - 5; // 在前一次坐标的基础上随机增减 x 坐标
        y = prevY + Math.floor(Math.random() * 10) - 5; // 在前一次坐标的基础上随机增减 y 坐标
        x = Math.max(0, Math.min(1000, x)); // 限制 x 坐标在 0 到 1000 之间
        y = Math.max(0, Math.min(800, y)); // 限制 y 坐标在 0 到 800 之间
        const eventType = i % 2 === 0 ? "pointermove" : "mousemove"; // 交替生成 "pointermove" 和 "mousemove"
    
        // 生成动作并添加到 data 数组中
        data.push(["move", x, y, prevTimestamp + Math.floor(Math.random() * 50) + 1, eventType]);
        if (i % 5 == 0 && i > numActions - 35 && mmm > 0) {
            data.push(["down", x, y, prevTimestamp + Math.floor(Math.random() * 50) + 1, "pointerdown"]);
        }
        if (i % 7 == 0 && i > numActions - 35 && mmm > 0) {
            mmm -= 1;
            data.push(["up", x, y, prevTimestamp + Math.floor(Math.random() * 50) + 1, "pointerup"]);
        }
        if ( i === numActions - 3 ){
            data.push(["focus",  prevTimestamp + Math.floor(Math.random() * 50) + 1]);
        }
    
    
        prevX = x; // 更新前一次的 x 坐标
        prevY = y; // 更新前一次的 y 坐标
        prevTimestamp = data[i][3]; // 更新上一个动作的时间戳
    }


    return data;
}



eee= [
    [
        "move",
        763,
        20,
        1711321107177,
        "pointermove"
    ],
    [
        "move",
        763,
        20,
        1711321107178,
        "mousemove"
    ],
    [
        "move",
        760,
        23,
        1711321107183,
        "pointermove"
    ],
    [
        "move",
        758,
        25,
        1711321107194,
        "pointermove"
    ],
    [
        "move",
        754,
        28,
        1711321107200,
        "pointermove"
    ],
    [
        "move",
        726,
        53,
        1711321107233,
        "pointermove"
    ],
    [
        "move",
        718,
        61,
        1711321107242,
        "pointermove"
    ],
    [
        "move",
        710,
        68,
        1711321107247,
        "pointermove"
    ],
    [
        "move",
        701,
        76,
        1711321107260,
        "pointermove"
    ],
    [
        "move",
        697,
        81,
        1711321107263,
        "pointermove"
    ],
    [
        "move",
        696,
        80,
        1711321107264,
        "mousemove"
    ],
    [
        "move",
        689,
        88,
        1711321107272,
        "pointermove"
    ],
    [
        "move",
        682,
        94,
        1711321107280,
        "pointermove"
    ],
    [
        "move",
        675,
        101,
        1711321107288,
        "pointermove"
    ],
    [
        "move",
        670,
        105,
        1711321107296,
        "pointermove"
    ],
    [
        "move",
        668,
        107,
        1711321107305,
        "pointermove"
    ],
    [
        "move",
        664,
        110,
        1711321107313,
        "pointermove"
    ],
    [
        "move",
        661,
        113,
        1711321107321,
        "pointermove"
    ],
    [
        "move",
        659,
        115,
        1711321107329,
        "pointermove"
    ],
    [
        "move",
        658,
        116,
        1711321107337,
        "pointermove"
    ],
    [
        "move",
        657,
        117,
        1711321107348,
        "pointermove"
    ],
    [
        "move",
        657,
        118,
        1711321107353,
        "pointermove"
    ],
    [
        "move",
        656,
        118,
        1711321107363,
        "pointermove"
    ],
    [
        "move",
        656,
        118,
        1711321107369,
        "pointermove"
    ],
    [
        "move",
        656,
        119,
        1711321107377,
        "pointermove"
    ],
    [
        "move",
        656,
        119,
        1711321107385,
        "pointermove"
    ],
    [
        "move",
        655,
        119,
        1711321107386,
        "mousemove"
    ],
    [
        "move",
        656,
        119,
        1711321107394,
        "pointermove"
    ],
    [
        "move",
        656,
        120,
        1711321107402,
        "pointermove"
    ],
    [
        "move",
        656,
        120,
        1711321107411,
        "pointermove"
    ],
    [
        "move",
        656,
        121,
        1711321107419,
        "pointermove"
    ],
    [
        "move",
        656,
        121,
        1711321107427,
        "pointermove"
    ],
    [
        "move",
        656,
        121,
        1711321107435,
        "pointermove"
    ],
    [
        "move",
        656,
        122,
        1711321107443,
        "pointermove"
    ],
    [
        "move",
        656,
        122,
        1711321107461,
        "pointermove"
    ],
    [
        "move",
        655,
        123,
        1711321107462,
        "pointermove"
    ],
    [
        "move",
        655,
        124,
        1711321107466,
        "pointermove"
    ],
    [
        "move",
        654,
        125,
        1711321107476,
        "pointermove"
    ],
    [
        "move",
        654,
        125,
        1711321107482,
        "pointermove"
    ],
    [
        "move",
        653,
        125,
        1711321107483,
        "mousemove"
    ],
    [
        "move",
        653,
        126,
        1711321107493,
        "pointermove"
    ],
    [
        "move",
        653,
        127,
        1711321107498,
        "pointermove"
    ],
    [
        "move",
        652,
        127,
        1711321107499,
        "mousemove"
    ],
    [
        "move",
        652,
        128,
        1711321107510,
        "pointermove"
    ],
    [
        "move",
        651,
        129,
        1711321107515,
        "pointermove"
    ],
    [
        "move",
        651,
        129,
        1711321107527,
        "pointermove"
    ],
    [
        "move",
        650,
        130,
        1711321107530,
        "pointermove"
    ],
    [
        "move",
        650,
        130,
        1711321107543,
        "pointermove"
    ],
    [
        "move",
        649,
        131,
        1711321107547,
        "pointermove"
    ],
    [
        "move",
        649,
        131,
        1711321107555,
        "pointermove"
    ],
    [
        "move",
        648,
        132,
        1711321107563,
        "pointermove"
    ],
    [
        "move",
        648,
        132,
        1711321107571,
        "pointermove"
    ],
    [
        "move",
        647,
        132,
        1711321107579,
        "pointermove"
    ],
    [
        "move",
        647,
        133,
        1711321107589,
        "pointermove"
    ],
    [
        "move",
        647,
        133,
        1711321107596,
        "pointermove"
    ],
    [
        "move",
        647,
        133,
        1711321107603,
        "pointermove"
    ],
    [
        "move",
        647,
        133,
        1711321107645,
        "pointermove"
    ],
    [
        "move",
        648,
        133,
        1711321107653,
        "pointermove"
    ],
    [
        "move",
        648,
        133,
        1711321107936,
        "pointermove"
    ],
    [
        "move",
        646,
        133,
        1711321107943,
        "pointermove"
    ],
    [
        "move",
        643,
        133,
        1711321107951,
        "pointermove"
    ],
    [
        "move",
        641,
        134,
        1711321107961,
        "pointermove"
    ],
    [
        "move",
        637,
        135,
        1711321107968,
        "pointermove"
    ],
    [
        "move",
        634,
        136,
        1711321107977,
        "pointermove"
    ],
    [
        "move",
        634,
        135,
        1711321107978,
        "mousemove"
    ],
    [
        "move",
        631,
        137,
        1711321107984,
        "pointermove"
    ],
    [
        "move",
        627,
        138,
        1711321107993,
        "pointermove"
    ],
    [
        "move",
        627,
        138,
        1711321107994,
        "mousemove"
    ],
    [
        "move",
        624,
        139,
        1711321107999,
        "pointermove"
    ],
    [
        "move",
        623,
        139,
        1711321108000,
        "mousemove"
    ],
    [
        "move",
        619,
        141,
        1711321108009,
        "pointermove"
    ],
    [
        "move",
        616,
        142,
        1711321108016,
        "pointermove"
    ],
    [
        "move",
        614,
        143,
        1711321108028,
        "pointermove"
    ],
    [
        "move",
        610,
        144,
        1711321108032,
        "pointermove"
    ],
    [
        "move",
        607,
        145,
        1711321108043,
        "pointermove"
    ],
    [
        "move",
        605,
        146,
        1711321108048,
        "pointermove"
    ],
    [
        "move",
        603,
        146,
        1711321108059,
        "pointermove"
    ],
    [
        "move",
        601,
        147,
        1711321108064,
        "pointermove"
    ],
    [
        "move",
        600,
        147,
        1711321108076,
        "pointermove"
    ],
    [
        "move",
        598,
        148,
        1711321108080,
        "pointermove"
    ],
    [
        "move",
        597,
        148,
        1711321108088,
        "pointermove"
    ],
    [
        "move",
        597,
        148,
        1711321108096,
        "pointermove"
    ],
    [
        "move",
        596,
        149,
        1711321108104,
        "pointermove"
    ],
    [
        "move",
        595,
        149,
        1711321108113,
        "pointermove"
    ],
    [
        "move",
        595,
        149,
        1711321108121,
        "pointermove"
    ],
    [
        "move",
        594,
        149,
        1711321108129,
        "pointermove"
    ],
    [
        "move",
        594,
        149,
        1711321108137,
        "pointermove"
    ],
    [
        "move",
        594,
        149,
        1711321108145,
        "pointermove"
    ],
    [
        "move",
        593,
        149,
        1711321108153,
        "pointermove"
    ],
    [
        "move",
        593,
        149,
        1711321108161,
        "pointermove"
    ],
    [
        "move",
        593,
        149,
        1711321108170,
        "pointermove"
    ],
    [
        "move",
        593,
        149,
        1711321108178,
        "pointermove"
    ],
    [
        "move",
        592,
        149,
        1711321108186,
        "pointermove"
    ],
    [
        "move",
        593,
        149,
        1711321108260,
        "pointermove"
    ],
    [
        "move",
        593,
        149,
        1711321108266,
        "pointermove"
    ],
    [
        "move",
        594,
        149,
        1711321108276,
        "pointermove"
    ],
    [
        "move",
        595,
        149,
        1711321108283,
        "pointermove"
    ],
    [
        "move",
        595,
        149,
        1711321108294,
        "pointermove"
    ],
    [
        "move",
        596,
        149,
        1711321108299,
        "pointermove"
    ],
    [
        "move",
        596,
        149,
        1711321108310,
        "pointermove"
    ],
    [
        "move",
        597,
        148,
        1711321108314,
        "pointermove"
    ],
    [
        "move",
        597,
        148,
        1711321108326,
        "pointermove"
    ],
    [
        "move",
        598,
        148,
        1711321108331,
        "pointermove"
    ],
    [
        "move",
        599,
        147,
        1711321108345,
        "pointermove"
    ],
    [
        "move",
        599,
        147,
        1711321108347,
        "pointermove"
    ],
    [
        "move",
        600,
        147,
        1711321108355,
        "pointermove"
    ],
    [
        "move",
        601,
        146,
        1711321108363,
        "pointermove"
    ],
    [
        "move",
        602,
        146,
        1711321108371,
        "pointermove"
    ],
    [
        "move",
        604,
        146,
        1711321108379,
        "pointermove"
    ],
    [
        "move",
        605,
        145,
        1711321108389,
        "pointermove"
    ],
    [
        "move",
        607,
        145,
        1711321108396,
        "pointermove"
    ],
    [
        "move",
        609,
        144,
        1711321108403,
        "pointermove"
    ],
    [
        "move",
        611,
        144,
        1711321108412,
        "pointermove"
    ],
    [
        "move",
        612,
        143,
        1711321108420,
        "pointermove"
    ],
    [
        "move",
        613,
        143,
        1711321108428,
        "pointermove"
    ],
    [
        "move",
        615,
        143,
        1711321108436,
        "pointermove"
    ],
    [
        "move",
        616,
        142,
        1711321108445,
        "pointermove"
    ],
    [
        "move",
        617,
        142,
        1711321108452,
        "pointermove"
    ],
    [
        "move",
        618,
        141,
        1711321108460,
        "pointermove"
    ],
    [
        "move",
        619,
        141,
        1711321108468,
        "pointermove"
    ],
    [
        "move",
        620,
        141,
        1711321108476,
        "pointermove"
    ],
    [
        "move",
        620,
        141,
        1711321108485,
        "pointermove"
    ],
    [
        "move",
        621,
        140,
        1711321108493,
        "pointermove"
    ],
    [
        "move",
        622,
        140,
        1711321108501,
        "pointermove"
    ],
    [
        "move",
        622,
        140,
        1711321108510,
        "pointermove"
    ],
    [
        "move",
        622,
        140,
        1711321108516,
        "pointermove"
    ],
    [
        "move",
        623,
        139,
        1711321108527,
        "pointermove"
    ],
    [
        "move",
        623,
        139,
        1711321108533,
        "pointermove"
    ],
    [
        "move",
        623,
        139,
        1711321108544,
        "pointermove"
    ],
    [
        "move",
        623,
        139,
        1711321108545,
        "mousemove"
    ],
    [
        "move",
        624,
        139,
        1711321108549,
        "pointermove"
    ],
    [
        "move",
        624,
        139,
        1711321108561,
        "pointermove"
    ],
    [
        "move",
        624,
        139,
        1711321108565,
        "pointermove"
    ],
    [
        "move",
        625,
        139,
        1711321108576,
        "pointermove"
    ],
    [
        "move",
        625,
        139,
        1711321108581,
        "pointermove"
    ],
    [
        "move",
        625,
        139,
        1711321108594,
        "pointermove"
    ],
    [
        "move",
        625,
        139,
        1711321108686,
        "pointermove"
    ],
    [
        "move",
        624,
        139,
        1711321108695,
        "pointermove"
    ],
    [
        "move",
        624,
        139,
        1711321108696,
        "mousemove"
    ],
    [
        "move",
        623,
        140,
        1711321108703,
        "pointermove"
    ],
    [
        "move",
        622,
        141,
        1711321108711,
        "pointermove"
    ],
    [
        "move",
        621,
        141,
        1711321108719,
        "pointermove"
    ],
    [
        "move",
        620,
        142,
        1711321108727,
        "pointermove"
    ],
    [
        "move",
        617,
        144,
        1711321108735,
        "pointermove"
    ],
    [
        "move",
        617,
        143,
        1711321108736,
        "mousemove"
    ],
    [
        "move",
        615,
        145,
        1711321108743,
        "pointermove"
    ],
    [
        "move",
        610,
        148,
        1711321108751,
        "pointermove"
    ],
    [
        "move",
        604,
        151,
        1711321108760,
        "pointermove"
    ],
    [
        "move",
        596,
        156,
        1711321108767,
        "pointermove"
    ],
    [
        "move",
        588,
        161,
        1711321108777,
        "pointermove"
    ],
    [
        "move",
        578,
        168,
        1711321108784,
        "pointermove"
    ],
    [
        "move",
        569,
        174,
        1711321108793,
        "pointermove"
    ],
    [
        "move",
        558,
        181,
        1711321108800,
        "pointermove"
    ],
    [
        "move",
        548,
        189,
        1711321108811,
        "pointermove"
    ],
    [
        "move",
        543,
        192,
        1711321108816,
        "pointermove"
    ],
    [
        "move",
        533,
        200,
        1711321108826,
        "pointermove"
    ],
    [
        "move",
        526,
        206,
        1711321108832,
        "pointermove"
    ],
    [
        "move",
        519,
        212,
        1711321108843,
        "pointermove"
    ],
    [
        "move",
        513,
        217,
        1711321108848,
        "pointermove"
    ],
    [
        "move",
        508,
        221,
        1711321108858,
        "pointermove"
    ],
    [
        "move",
        506,
        224,
        1711321108864,
        "pointermove"
    ],
    [
        "move",
        502,
        227,
        1711321108876,
        "pointermove"
    ],
    [
        "move",
        499,
        230,
        1711321108880,
        "pointermove"
    ],
    [
        "move",
        496,
        232,
        1711321108888,
        "pointermove"
    ],
    [
        "move",
        494,
        235,
        1711321108896,
        "pointermove"
    ],
    [
        "move",
        494,
        234,
        1711321108897,
        "mousemove"
    ],
    [
        "move",
        493,
        237,
        1711321108905,
        "pointermove"
    ],
    [
        "move",
        491,
        238,
        1711321108914,
        "pointermove"
    ],
    [
        "move",
        489,
        240,
        1711321108921,
        "pointermove"
    ],
    [
        "move",
        488,
        241,
        1711321108929,
        "pointermove"
    ],
    [
        "move",
        487,
        243,
        1711321108937,
        "pointermove"
    ],
    [
        "move",
        486,
        244,
        1711321108945,
        "pointermove"
    ],
    [
        "move",
        486,
        245,
        1711321108954,
        "pointermove"
    ],
    [
        "move",
        485,
        246,
        1711321108961,
        "pointermove"
    ],
    [
        "move",
        484,
        246,
        1711321108969,
        "pointermove"
    ],
    [
        "move",
        483,
        247,
        1711321108977,
        "pointermove"
    ],
    [
        "move",
        483,
        248,
        1711321108986,
        "pointermove"
    ],
    [
        "move",
        482,
        249,
        1711321108993,
        "pointermove"
    ],
    [
        "move",
        482,
        249,
        1711321109002,
        "pointermove"
    ],
    [
        "move",
        481,
        250,
        1711321109009,
        "pointermove"
    ],
    [
        "move",
        480,
        251,
        1711321109018,
        "pointermove"
    ],
    [
        "move",
        480,
        252,
        1711321109026,
        "pointermove"
    ],
    [
        "move",
        479,
        253,
        1711321109034,
        "pointermove"
    ],
    [
        "move",
        479,
        253,
        1711321109044,
        "pointermove"
    ],
    [
        "move",
        479,
        253,
        1711321109051,
        "pointermove"
    ],
    [
        "move",
        478,
        254,
        1711321109060,
        "pointermove"
    ],
    [
        "move",
        478,
        254,
        1711321109066,
        "pointermove"
    ],
    [
        "move",
        478,
        253,
        1711321109067,
        "mousemove"
    ],
    [
        "move",
        478,
        254,
        1711321109077,
        "pointermove"
    ],
    [
        "move",
        478,
        254,
        1711321109082,
        "pointermove"
    ],
    [
        "move",
        478,
        255,
        1711321109098,
        "pointermove"
    ],
    [
        "move",
        477,
        254,
        1711321109099,
        "mousemove"
    ],
    [
        "move",
        478,
        255,
        1711321109164,
        "pointermove"
    ],
    [
        "move",
        478,
        255,
        1711321109188,
        "pointermove"
    ],
    [
        "move",
        477,
        255,
        1711321109196,
        "pointermove"
    ],
    [
        "move",
        477,
        255,
        1711321109205,
        "pointermove"
    ],
    [
        "move",
        477,
        256,
        1711321109212,
        "pointermove"
    ],
    [
        "move",
        477,
        256,
        1711321109220,
        "pointermove"
    ],
    [
        "down",
        477,
        256,
        1711321109247,
        "pointerdown"
    ],
    [
        "up",
        477,
        256,
        1711321109327,
        "pointerup"
    ],
    [
        "move",
        477,
        256,
        1711321109543,
        "pointermove"
    ],
    [
        "move",
        478,
        254,
        1711321109551,
        "pointermove"
    ],
    [
        "move",
        481,
        251,
        1711321109559,
        "pointermove"
    ],
    [
        "move",
        485,
        247,
        1711321109567,
        "pointermove"
    ],
    [
        "move",
        491,
        241,
        1711321109581,
        "pointermove"
    ],
    [
        "move",
        498,
        234,
        1711321109583,
        "pointermove"
    ],
    [
        "move",
        507,
        227,
        1711321109593,
        "pointermove"
    ],
    [
        "move",
        515,
        219,
        1711321109599,
        "pointermove"
    ],
    [
        "move",
        526,
        209,
        1711321109609,
        "pointermove"
    ],
    [
        "move",
        537,
        200,
        1711321109616,
        "pointermove"
    ],
    [
        "move",
        548,
        190,
        1711321109626,
        "pointermove"
    ],
    [
        "move",
        561,
        181,
        1711321109634,
        "pointermove"
    ],
    [
        "move",
        566,
        177,
        1711321109642,
        "pointermove"
    ],
    [
        "move",
        576,
        169,
        1711321109648,
        "pointermove"
    ],
    [
        "move",
        585,
        162,
        1711321109659,
        "pointermove"
    ],
    [
        "move",
        593,
        157,
        1711321109664,
        "pointermove"
    ],
    [
        "move",
        600,
        152,
        1711321109672,
        "pointermove"
    ],
    [
        "move",
        600,
        151,
        1711321109673,
        "mousemove"
    ],
    [
        "move",
        607,
        148,
        1711321109680,
        "pointermove"
    ],
    [
        "move",
        613,
        144,
        1711321109689,
        "pointermove"
    ],
    [
        "move",
        618,
        140,
        1711321109696,
        "pointermove"
    ],
    [
        "move",
        623,
        137,
        1711321109704,
        "pointermove"
    ],
    [
        "move",
        627,
        135,
        1711321109712,
        "pointermove"
    ],
    [
        "move",
        629,
        134,
        1711321109721,
        "pointermove"
    ],
    [
        "move",
        635,
        130,
        1711321109729,
        "pointermove"
    ],
    [
        "move",
        636,
        129,
        1711321109736,
        "pointermove"
    ],
    [
        "move",
        639,
        127,
        1711321109745,
        "pointermove"
    ],
    [
        "move",
        642,
        125,
        1711321109752,
        "pointermove"
    ],
    [
        "move",
        641,
        125,
        1711321109753,
        "mousemove"
    ],
    [
        "move",
        644,
        124,
        1711321109761,
        "pointermove"
    ],
    [
        "move",
        645,
        123,
        1711321109768,
        "pointermove"
    ],
    [
        "move",
        646,
        122,
        1711321109777,
        "pointermove"
    ],
    [
        "move",
        647,
        121,
        1711321109785,
        "pointermove"
    ],
    [
        "move",
        648,
        121,
        1711321109793,
        "pointermove"
    ],
    [
        "move",
        648,
        121,
        1711321109801,
        "pointermove"
    ],
    [
        "move",
        648,
        120,
        1711321109809,
        "pointermove"
    ],
    [
        "move",
        649,
        120,
        1711321109817,
        "pointermove"
    ],
    [
        "move",
        649,
        120,
        1711321109825,
        "pointermove"
    ],
    [
        "move",
        649,
        120,
        1711321109833,
        "pointermove"
    ],
    [
        "move",
        649,
        120,
        1711321109858,
        "pointermove"
    ],
    [
        "move",
        649,
        119,
        1711321109882,
        "pointermove"
    ],
    [
        "move",
        649,
        119,
        1711321109891,
        "pointermove"
    ],
    [
        "move",
        649,
        119,
        1711321109898,
        "pointermove"
    ],
    [
        "move",
        649,
        119,
        1711321109914,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321109925,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321109930,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321109938,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321109946,
        "pointermove"
    ],
    [
        "move",
        650,
        117,
        1711321109954,
        "pointermove"
    ],
    [
        "move",
        650,
        117,
        1711321109971,
        "pointermove"
    ],
    [
        "move",
        650,
        117,
        1711321110084,
        "pointermove"
    ],
    [
        "move",
        650,
        118,
        1711321110142,
        "pointermove"
    ],
    [
        "move",
        650,
        118,
        1711321110189,
        "pointermove"
    ],
    [
        "move",
        650,
        118,
        1711321110213,
        "pointermove"
    ],
    [
        "move",
        650,
        118,
        1711321110221,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321110237,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321110253,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321110254,
        "mousemove"
    ],
    [
        "move",
        649,
        118,
        1711321110262,
        "pointermove"
    ],
    [
        "move",
        649,
        118,
        1711321110278,
        "pointermove"
    ],
    [
        "move",
        649,
        119,
        1711321110294,
        "pointermove"
    ],
    [
        "move",
        649,
        119,
        1711321110318,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110351,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110410,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110442,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110464,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110481,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110492,
        "pointermove"
    ],
    [
        "move",
        648,
        119,
        1711321110496,
        "pointermove"
    ],
    [
        "down",
        648,
        119,
        1711321110529,
        "pointerdown"
    ],
    [
        "up",
        648,
        119,
        1711321110626,
        "pointerup"
    ],
    [
        "move",
        647,
        119,
        1711321110844,
        "pointermove"
    ],
    [
        "move",
        645,
        120,
        1711321110851,
        "pointermove"
    ],
    [
        "move",
        639,
        124,
        1711321110859,
        "pointermove"
    ],
    [
        "move",
        634,
        126,
        1711321110867,
        "pointermove"
    ],
    [
        "move",
        633,
        126,
        1711321110868,
        "mousemove"
    ],
    [
        "move",
        627,
        131,
        1711321110876,
        "pointermove"
    ],
    [
        "move",
        618,
        136,
        1711321110884,
        "pointermove"
    ],
    [
        "move",
        611,
        141,
        1711321110894,
        "pointermove"
    ],
    [
        "move",
        606,
        143,
        1711321110900,
        "pointermove"
    ],
    [
        "move",
        598,
        148,
        1711321110909,
        "pointermove"
    ],
    [
        "move",
        591,
        153,
        1711321110916,
        "pointermove"
    ],
    [
        "move",
        583,
        157,
        1711321110925,
        "pointermove"
    ],
    [
        "move",
        576,
        161,
        1711321110932,
        "pointermove"
    ],
    [
        "move",
        570,
        165,
        1711321110942,
        "pointermove"
    ],
    [
        "move",
        564,
        168,
        1711321110948,
        "pointermove"
    ],
    [
        "move",
        559,
        170,
        1711321110959,
        "pointermove"
    ],
    [
        "move",
        555,
        173,
        1711321110964,
        "pointermove"
    ],
    [
        "move",
        551,
        175,
        1711321110975,
        "pointermove"
    ],
    [
        "move",
        547,
        177,
        1711321110980,
        "pointermove"
    ],
    [
        "move",
        545,
        178,
        1711321110992,
        "pointermove"
    ],
    [
        "move",
        541,
        181,
        1711321110997,
        "pointermove"
    ],
    [
        "move",
        539,
        182,
        1711321111005,
        "pointermove"
    ],
    [
        "move",
        537,
        184,
        1711321111013,
        "pointermove"
    ],
    [
        "move",
        534,
        185,
        1711321111021,
        "pointermove"
    ],
    [
        "move",
        532,
        186,
        1711321111029,
        "pointermove"
    ],
    [
        "move",
        531,
        188,
        1711321111037,
        "pointermove"
    ],
    [
        "move",
        529,
        189,
        1711321111045,
        "pointermove"
    ],
    [
        "move",
        527,
        190,
        1711321111053,
        "pointermove"
    ],
    [
        "move",
        525,
        191,
        1711321111062,
        "pointermove"
    ],
    [
        "move",
        523,
        192,
        1711321111070,
        "pointermove"
    ],
    [
        "move",
        521,
        193,
        1711321111078,
        "pointermove"
    ],
    [
        "move",
        520,
        194,
        1711321111086,
        "pointermove"
    ],
    [
        "move",
        518,
        195,
        1711321111094,
        "pointermove"
    ],
    [
        "move",
        517,
        196,
        1711321111102,
        "pointermove"
    ],
    [
        "move",
        516,
        196,
        1711321111110,
        "pointermove"
    ],
    [
        "move",
        515,
        197,
        1711321111118,
        "pointermove"
    ],
    [
        "move",
        514,
        197,
        1711321111126,
        "pointermove"
    ],
    [
        "move",
        513,
        197,
        1711321111127,
        "mousemove"
    ],
    [
        "move",
        513,
        198,
        1711321111135,
        "pointermove"
    ],
    [
        "move",
        513,
        198,
        1711321111144,
        "pointermove"
    ],
    [
        "move",
        512,
        198,
        1711321111152,
        "pointermove"
    ],
    [
        "move",
        512,
        198,
        1711321111161,
        "pointermove"
    ],
    [
        "move",
        512,
        199,
        1711321111168,
        "pointermove"
    ],
    [
        "move",
        511,
        199,
        1711321111177,
        "pointermove"
    ],
    [
        "move",
        511,
        199,
        1711321111183,
        "pointermove"
    ],
    [
        "move",
        511,
        199,
        1711321111193,
        "pointermove"
    ],
    [
        "move",
        511,
        199,
        1711321111200,
        "pointermove"
    ],
    [
        "move",
        510,
        199,
        1711321111210,
        "pointermove"
    ],
    [
        "move",
        510,
        199,
        1711321111215,
        "pointermove"
    ],
    [
        "move",
        510,
        199,
        1711321111226,
        "pointermove"
    ],
    [
        "move",
        509,
        199,
        1711321111264,
        "pointermove"
    ],
    [
        "move",
        509,
        199,
        1711321111265,
        "pointermove"
    ],
    [
        "down",
        509,
        199,
        1711321111294,
        "pointerdown"
    ],
    [
        "move",
        509,
        200,
        1711321111295,
        "pointermove"
    ],
    [
        "up",
        509,
        200,
        1711321111393,
        "pointerup"
    ],
    [
        "move",
        509,
        200,
        1711321111397,
        "pointermove"
    ],
    [
        "move",
        509,
        200,
        1711321111571,
        "pointermove"
    ],
    [
        "move",
        511,
        196,
        1711321111579,
        "pointermove"
    ],
    [
        "move",
        513,
        195,
        1711321111586,
        "pointermove"
    ],
    [
        "move",
        513,
        194,
        1711321111587,
        "mousemove"
    ],
    [
        "move",
        516,
        191,
        1711321111595,
        "pointermove"
    ],
    [
        "move",
        520,
        188,
        1711321111603,
        "pointermove"
    ],
    [
        "move",
        524,
        185,
        1711321111611,
        "pointermove"
    ],
    [
        "move",
        523,
        184,
        1711321111612,
        "mousemove"
    ],
    [
        "move",
        529,
        179,
        1711321111619,
        "pointermove"
    ],
    [
        "move",
        533,
        176,
        1711321111627,
        "pointermove"
    ],
    [
        "move",
        538,
        171,
        1711321111635,
        "pointermove"
    ],
    [
        "move",
        542,
        167,
        1711321111643,
        "pointermove"
    ],
    [
        "move",
        546,
        163,
        1711321111651,
        "pointermove"
    ],
    [
        "move",
        547,
        162,
        1711321111660,
        "pointermove"
    ],
    [
        "move",
        550,
        158,
        1711321111668,
        "pointermove"
    ],
    [
        "move",
        553,
        155,
        1711321111677,
        "pointermove"
    ],
    [
        "move",
        555,
        153,
        1711321111684,
        "pointermove"
    ],
    [
        "move",
        557,
        151,
        1711321111693,
        "pointermove"
    ],
    [
        "move",
        558,
        149,
        1711321111700,
        "pointermove"
    ],
    [
        "move",
        559,
        148,
        1711321111709,
        "pointermove"
    ],
    [
        "move",
        560,
        148,
        1711321111716,
        "pointermove"
    ],
    [
        "move",
        560,
        147,
        1711321111727,
        "pointermove"
    ],
    [
        "move",
        561,
        146,
        1711321111732,
        "pointermove"
    ],
    [
        "move",
        561,
        146,
        1711321111744,
        "pointermove"
    ],
    [
        "move",
        562,
        146,
        1711321111749,
        "pointermove"
    ],
    [
        "move",
        562,
        146,
        1711321111760,
        "pointermove"
    ],
    [
        "move",
        562,
        145,
        1711321111765,
        "pointermove"
    ],
    [
        "move",
        562,
        145,
        1711321111776,
        "pointermove"
    ],
    [
        "move",
        563,
        145,
        1711321111781,
        "pointermove"
    ],
    [
        "move",
        563,
        145,
        1711321111793,
        "pointermove"
    ],
    [
        "move",
        563,
        144,
        1711321111797,
        "pointermove"
    ],
    [
        "move",
        564,
        144,
        1711321111805,
        "pointermove"
    ],
    [
        "move",
        564,
        143,
        1711321111815,
        "pointermove"
    ],
    [
        "move",
        565,
        143,
        1711321111823,
        "pointermove"
    ],
    [
        "move",
        565,
        142,
        1711321111830,
        "pointermove"
    ],
    [
        "move",
        564,
        142,
        1711321111831,
        "mousemove"
    ],
    [
        "move",
        565,
        141,
        1711321111839,
        "pointermove"
    ],
    [
        "move",
        566,
        141,
        1711321111847,
        "pointermove"
    ],
    [
        "move",
        567,
        140,
        1711321111855,
        "pointermove"
    ],
    [
        "move",
        567,
        139,
        1711321111862,
        "pointermove"
    ],
    [
        "move",
        568,
        138,
        1711321111870,
        "pointermove"
    ],
    [
        "move",
        568,
        137,
        1711321111879,
        "pointermove"
    ],
    [
        "move",
        569,
        136,
        1711321111887,
        "pointermove"
    ],
    [
        "move",
        568,
        136,
        1711321111888,
        "mousemove"
    ],
    [
        "move",
        569,
        136,
        1711321111894,
        "pointermove"
    ],
    [
        "move",
        570,
        135,
        1711321111903,
        "pointermove"
    ],
    [
        "move",
        570,
        135,
        1711321111911,
        "pointermove"
    ],
    [
        "down",
        570,
        135,
        1711321111944,
        "pointerdown"
    ],
    [
        "move",
        570,
        135,
        1711321111944,
        "pointermove"
    ],
    [
        "up",
        570,
        135,
        1711321112028,
        "pointerup"
    ],
    [
        "move",
        570,
        135,
        1711321112032,
        "pointermove"
    ],
    [
        "move",
        570,
        135,
        1711321112185,
        "pointermove"
    ],
    [
        "move",
        570,
        138,
        1711321112193,
        "pointermove"
    ],
    [
        "move",
        570,
        143,
        1711321112201,
        "pointermove"
    ],
    [
        "move",
        572,
        146,
        1711321112209,
        "pointermove"
    ],
    [
        "move",
        573,
        151,
        1711321112217,
        "pointermove"
    ],
    [
        "move",
        575,
        155,
        1711321112226,
        "pointermove"
    ],
    [
        "move",
        576,
        160,
        1711321112233,
        "pointermove"
    ],
    [
        "move",
        578,
        169,
        1711321112241,
        "pointermove"
    ],
    [
        "move",
        581,
        179,
        1711321112249,
        "pointermove"
    ],
    [
        "move",
        582,
        184,
        1711321112259,
        "pointermove"
    ],
    [
        "move",
        584,
        194,
        1711321112265,
        "pointermove"
    ],
    [
        "move",
        584,
        203,
        1711321112275,
        "pointermove"
    ],
    [
        "move",
        586,
        214,
        1711321112281,
        "pointermove"
    ],
    [
        "move",
        587,
        230,
        1711321112291,
        "pointermove"
    ],
    [
        "move",
        587,
        241,
        1711321112298,
        "pointermove"
    ],
    [
        "move",
        587,
        262,
        1711321112308,
        "pointermove"
    ],
    [
        "scroll",
        586,
        264,
        1711321112459,
        null
    ],
    [
        "scroll",
        586,
        269,
        1711321112475,
        null
    ],
    [
        "scroll",
        586,
        282,
        1711321112493,
        null
    ],
    [
        "scroll",
        586,
        294,
        1711321112508,
        null
    ],
    [
        "scroll",
        586,
        320,
        1711321112525,
        null
    ],
    [
        "scroll",
        586,
        324,
        1711321112543,
        null
    ],
    [
        "scroll",
        586,
        339,
        1711321112558,
        null
    ],
    [
        "scroll",
        586,
        340,
        1711321112575,
        null
    ],
    [
        "scroll",
        586,
        345,
        1711321112592,
        null
    ],
    [
        "scroll",
        586,
        347,
        1711321112609,
        null
    ],
    [
        "scroll",
        586,
        347,
        1711321112627,
        null
    ],
    [
        "scroll",
        586,
        347,
        1711321112643,
        null
    ],
    [
        "scroll",
        586,
        348,
        1711321112659,
        null
    ],
    [
        "scroll",
        586,
        349,
        1711321112692,
        null
    ],
    [
        "scroll",
        586,
        350,
        1711321112710,
        null
    ],
    [
        "move",
        587,
        262,
        1711321112859,
        "pointermove"
    ],
    [
        "move",
        589,
        265,
        1711321112864,
        "pointermove"
    ],
    [
        "move",
        591,
        267,
        1711321112872,
        "pointermove"
    ],
    [
        "move",
        593,
        270,
        1711321112881,
        "pointermove"
    ],
    [
        "move",
        596,
        273,
        1711321112888,
        "pointermove"
    ],
    [
        "move",
        598,
        277,
        1711321112897,
        "pointermove"
    ],
    [
        "move",
        601,
        280,
        1711321112904,
        "pointermove"
    ],
    [
        "move",
        603,
        282,
        1711321112913,
        "pointermove"
    ],
    [
        "move",
        604,
        284,
        1711321112921,
        "pointermove"
    ],
    [
        "move",
        606,
        287,
        1711321112929,
        "pointermove"
    ],
    [
        "move",
        608,
        289,
        1711321112937,
        "pointermove"
    ],
    [
        "move",
        610,
        291,
        1711321112945,
        "pointermove"
    ],
    [
        "move",
        611,
        293,
        1711321112953,
        "pointermove"
    ],
    [
        "move",
        613,
        295,
        1711321112961,
        "pointermove"
    ],
    [
        "move",
        614,
        297,
        1711321112969,
        "pointermove"
    ],
    [
        "move",
        615,
        298,
        1711321112977,
        "pointermove"
    ],
    [
        "move",
        616,
        300,
        1711321112985,
        "pointermove"
    ],
    [
        "move",
        617,
        302,
        1711321112993,
        "pointermove"
    ],
    [
        "move",
        618,
        303,
        1711321113002,
        "pointermove"
    ],
    [
        "move",
        619,
        305,
        1711321113011,
        "pointermove"
    ],
    [
        "move",
        620,
        307,
        1711321113017,
        "pointermove"
    ],
    [
        "move",
        621,
        308,
        1711321113026,
        "pointermove"
    ],
    [
        "move",
        622,
        310,
        1711321113034,
        "pointermove"
    ],
    [
        "move",
        623,
        311,
        1711321113046,
        "pointermove"
    ],
    [
        "move",
        623,
        313,
        1711321113050,
        "pointermove"
    ],
    [
        "move",
        624,
        315,
        1711321113061,
        "pointermove"
    ],
    [
        "move",
        624,
        316,
        1711321113066,
        "pointermove"
    ],
    [
        "move",
        625,
        317,
        1711321113075,
        "pointermove"
    ],
    [
        "move",
        625,
        318,
        1711321113081,
        "pointermove"
    ],
    [
        "move",
        626,
        319,
        1711321113092,
        "pointermove"
    ],
    [
        "move",
        626,
        320,
        1711321113098,
        "pointermove"
    ],
    [
        "move",
        626,
        321,
        1711321113110,
        "pointermove"
    ],
    [
        "move",
        627,
        322,
        1711321113114,
        "pointermove"
    ],
    [
        "move",
        627,
        322,
        1711321113125,
        "pointermove"
    ],
    [
        "move",
        627,
        323,
        1711321113130,
        "pointermove"
    ],
    [
        "move",
        627,
        323,
        1711321113139,
        "pointermove"
    ],
    [
        "move",
        628,
        324,
        1711321113147,
        "pointermove"
    ],
    [
        "move",
        628,
        324,
        1711321113155,
        "pointermove"
    ],
    [
        "move",
        628,
        324,
        1711321113164,
        "pointermove"
    ],
    [
        "down",
        628,
        324,
        1711321113194,
        "pointerdown"
    ],
    [
        "focus",
        1711321113195
    ],
    [
        "move",
        628,
        324,
        1711321113195,
        "pointermove"
    ],
    [
        "up",
        628,
        324,
        1711321113316,
        "pointerup"
    ],
    [
        "move",
        628,
        325,
        1711321113320,
        "pointermove"
    ]
]



function MD5_Encrypt(word) {
  return CryptoJS.MD5(word).toString();
}


function RSA_encrypt(data) {
  const public_key_1 = '00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81';
  const public_key_2 = '10001';
  const public_key = new NodeRSA();
  public_key.importKey({
      n: Buffer.from(public_key_1, 'hex'),
      e: parseInt(public_key_2, 16),
  }, 'components-public');
  const encrypted = crypto.publicEncrypt({
      key: public_key.exportKey('public'),
      padding: crypto.constants.RSA_PKCS1_PADDING
  }, Buffer.from(data));
  return encrypted.toString('hex');
}


function get_key() {
    var s4 = "";
    for (i = 0; i < 4; i++) {
        s4 = s4 + (65536 * (1 + Math["random"]()) | 0)["toString"](16)["substring"](1);
    }
    return s4;
}

ww = {
  "$_DAH": {
    "$_DBV": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()",
    "$_DCS": ".",
    "$_DDU": 7274496,
    "$_DEf": 9483264,
    "$_DFC": 19220,
    "$_DG_": 235,
    "$_DHY": 24
  },
  "$_DBV": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()",
  "$_DCS": ".",
  "$_DDU": 7274496,
  "$_DEf": 9483264,
  "$_DFC": 19220,
  "$_DG_": 235,
  "$_DHY": 24,
  "$_DIG": function (e) {
    for (var t = [], n = 0, r = e["length"]; n < r; n += 1) t["push"](e["charCodeAt"](n));
    return t;
  },
  "$_DJx": function (e) {
    for (var t = "", n = 0, r = e["length"]; n < r; n += 1) t += String["fromCharCode"](e[n]);
    return t;
  },
  "$_EAu": function (e) {
    var t = this["$_DBV"];
    return e < 0 || e >= t["length"] ? "." : t["charAt"](e);
  },
  "$_EBs": function (e) {
    return this["$_DBV"]["indexOf"](e);
  },
  "$_ECc": function (e, t) {
    return e >> t & 1;
  },
  "$_EDb": function (e, i) {
    var s = this;
    i || (i = s);
    for (var t = function (e, t) {
        for (var n = 0, r = i["$_DHY"] - 1; 0 <= r; r -= 1) 1 === s["$_ECc"](t, r) && (n = (n << 1) + s["$_ECc"](e, r));
        return n;
      }, n = "", r = "", o = e["length"], _ = 0; _ < o; _ += 3) {
      var a;
      if (_ + 2 < o) a = (e[_] << 16) + (e[_ + 1] << 8) + e[_ + 2], n += s["$_EAu"](t(a, i["$_DDU"])) + s["$_EAu"](t(a, i["$_DEf"])) + s["$_EAu"](t(a, i["$_DFC"])) + s["$_EAu"](t(a, i["$_DG_"]));else {
        var c = o % 3;
        2 == c ? (a = (e[_] << 16) + (e[_ + 1] << 8), n += s["$_EAu"](t(a, i["$_DDU"])) + s["$_EAu"](t(a, i["$_DEf"])) + s["$_EAu"](t(a, i["$_DFC"])), r = i["$_DCS"]) : 1 == c && (a = e[_] << 16, n += s["$_EAu"](t(a, i["$_DDU"])) + s["$_EAu"](t(a, i["$_DEf"])), r = i["$_DCS"] + i["$_DCS"]);
      }
    }
    return {
      "res": n,
      "end": r
    };
  },
  "$_EEs": function (e) {
    var t = this["$_EDb"](this["$_DIG"](e));
    return t["res"] + t["end"];
  },
  "$_EFO": function (e) {
    var t = this["$_EDb"](e);
    return t["res"] + t["end"];
  },
  "$_EGQ": function (e, s) {
    var o = this;
    s || (s = o);
    for (var t = function (e, t) {
        var $_GGFC = vjekb.$_CV,
          $_GGEh = ['$_GGIv'].concat($_GGFC),
          $_GGGu = $_GGEh[1];
        $_GGEh.shift();
        var $_GGHa = $_GGEh[0];
        if (e < 0) return 0;
        for (var n = 5, r = 0, i = s["$_DHY"] - 1; 0 <= i; i -= 1) 1 === o["$_ECc"](t, i) && (r += o["$_ECc"](e, n) << i, n -= 1);
        return r;
      }, n = e["length"], r = "", i = 0; i < n; i += 4) {
      var _ = t(o["$_EBs"](e["charAt"](i)), s["$_DDU"]) + t(o["$_EBs"](e["charAt"](i + 1)), s["$_DEf"]) + t(o["$_EBs"](e["charAt"](i + 2)), s["$_DFC"]) + t(o["$_EBs"](e["charAt"](i + 3)), s["$_DG_"]),
        a = _ >> 16 & 255;
      if (r += String["fromCharCode"](a), e["charAt"](i + 2) !== s["$_DCS"]) {
        var c = _ >> 8 & 255;
        if (r += String["fromCharCode"](c), e["charAt"](i + 3) !== s["$_DCS"]) {
          var l = 255 & _;
          r += String["fromCharCode"](l);
        }
      }
    }
    return r;
  },
  "$_EHE": function (e) {
    var t = 4 - e["length"] % 4;
    if (t < 4) for (var n = 0; n < t; n += 1) e += this["$_DCS"];
    return this["$_EGQ"](e);
  },
  "$_EIZ": function (e) {
    return this["$_EHE"](e);
  }
}



function AES_Encrypt(o_text, random_str) {
  var key = CryptoJS.enc.Utf8.parse(random_str);
  var iv = CryptoJS.enc.Utf8.parse("0000000000000000");
  var srcs = CryptoJS.enc.Utf8.parse(o_text);
  var encrypted = CryptoJS.AES.encrypt(srcs, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
  });
  for (var r = encrypted, o = r.ciphertext.words, i = r.ciphertext.sigBytes, s = [], a = 0; a < i; a++) {
      var c = o[a >>> 2] >>> 24 - a % 4 * 8 & 255;
      s.push(c);
  }
  return s;
};



t = {
  "x": 196.296875,
  "y": 306.625,
  "width": 333.3828125,
  "height": 333.3828125,
  "top": 306.625,
  "right": 529.6796875,
  "bottom": 640.0078125,
  "left": 196.296875
}




function generateTimingData() {
  currentTime = Date.now();
  return {
    "a": currentTime + 4898,
    "b": currentTime + 5285,
    "c": currentTime + 5285,
    "d": 0,
    "e": 0,
    "f": currentTime + 4940,
    "g": currentTime + 4940,
    "h": currentTime + 4940,
    "i": currentTime + 4944,
    "j": currentTime + 4959,
    "k": currentTime + 4952,
    "l": currentTime + 4959,
    "m": currentTime + 5279,
    "n": currentTime + 5315,
    "o": currentTime + 5291,
    "p": currentTime + 5621,
    "q": currentTime + 5694,
    "r": currentTime + 5695,
    "s": currentTime + 6240,
    "t": currentTime + 6240,
    "u": currentTime + 6260
  };
}


get_cat = function(pos){
  // 输入的坐标应该是 [[x1, y1], [x2, y2], [x3, y3], ...]
  
  ramdomtime_sum = 0
  ca = []
  for (i = 0; i < pos.length; i++) {
      ramdomtime = Math.floor(Math.random() * 1000) + 1000;
      p = pos[i]
      ca.push({
          "x": p[0] + t.x,
          "y": p[1] + t.y,
          "t": 0,
          "dt": ramdomtime, // 两次点击的时间间隔
      })
      ramdomtime_sum += ramdomtime
  }
  // 463, y: 664
  ramdomtime = Math.floor(Math.random() * 1000) + 1000;
  ca.push({
      "x": 267 + t.x,
      "y": 358 + t.y,
      "t": 3, // 如果点击确认按钮, 则 t = 3
      "dt": ramdomtime, 
  })
  ramdomtime_sum += ramdomtime

  return {
      "ca": ca,
      "timesum": ramdomtime_sum
  }

}


function poses2geetest(poses) {
  /**
   * 处理坐标，变为极验需要的样子
   * 参数:
   *   poses: list: 坐标信息, 格式是: [[x1, y1, x2, y2], [x1, y1, x2, y2], ...] 需要转为极验需要的格式
   * 返回:
   *   stringCodes: str: 极验需要的坐标信息, 格式是: "x1_y1,x2_y2,x3_y3" , 这里做了缩放
   *   centerxy: list: 中心点坐标, 格式是: [[x1, y1], [x2, y2], ...]
   *  
   */
  const newCoords = [];
  const centerxy = [];
  for (const pose of poses) {
      const x = (pose[0] + pose[2]) / 2;
      const y = (pose[1] + pose[3]) / 2;
      centerxy.push([x, y]);
      const final_x = Math.round(x / 333.375 * 100 * 100);
      const final_y = Math.round(y / 333.375 * 100 * 100);
      const final = `${final_x}_${final_y}`;
      newCoords.push(final);
  }
  const stringCodes = newCoords.join(',');
  
  return {
    "stringCodes": stringCodes,
    "centerxy": centerxy
  }
}



function get_w(poses, pic,  mygt, mychallenge, myc, mys) {
    /* poses: 点击的坐标, 传入格式是: [[x1, y1, x2, y2], [x1, y1, x2, y2], ...]
    * pic: 字符串
    * mygt: 字符串
    * mychallenge: 字符串
    * myc: 数组
    * mys: 字符串
    */

    romdon_key = get_key()

    newposes = poses2geetest(poses)
    stringCodes = newposes["stringCodes"]  // 转为需要的格式
    centerxy = newposes['centerxy']// 获取中心点坐标

    cat = get_cat(centerxy)
    ca = cat.ca

    // passtime = Math.floor(Math.random() * (3000 - 1000 + 1)) + 1000;
    
    passtime = cat.timesum + Math.floor(Math.random()*1000 + 3000)
    
    //// 采用模拟的 轨迹 ---虽然不检查, 但是还是模拟一下,看看是否有问题
    geshu = Math.floor(Math.random() * (80 + 1)) + 400

    eee = geteee(geshu, poses.length)

    /// 采用 copy的轨迹
    // eee = eee

    o = {
        "lang": "zh-cn",
        "passtime": passtime,
        "a": stringCodes, 
        "pic": pic,  
        "tt": function (e, t, n) {
          var r,
            i = 0,
            s = e,
            o = t[0],
            _ = t[2],
            a = t[4];
    
          while (r = n["substr"](i, 2)) {
            i += 2;
            var c = parseInt(r, 16),
              l = String["fromCharCode"](c),
              u = (o * c * c + _ * c + a) % e["length"];
            s = s["substr"](0, u) + l + s["substr"](u);
          }
          return s;
        }(pe["$_BGCW"](eee), myc, mys),
        "ep": {
          "ca": ca,
          "v": "3.1.0",
          "$_FB": false,
          "me": true,
          "tm": generateTimingData()
        },
        "h9s9": "1816378497",
    };
    o["rp"] = MD5_Encrypt(mygt + mychallenge + passtime)
    u = RSA_encrypt(romdon_key)
    xiyu = JSON.stringify(o).replace(" ", "").replace("'", '"')
    w = ww["$_EFO"](AES_Encrypt(xiyu, romdon_key))  + u
    return w
}










// gt = "ac597a4506fee079629df5d8b66dd4fe"
// challenge = "3054898f12f2d91e3aa7c54afdaf1e7f"
// pic = '/captcha_v3/batch/v3/65415/2024-03-23T19/word/384b1a0c983d4142b991f5f3bfaab5ea.jpg'
// code = "5033_5485,6740_3121"
// cc = [12, 58, 98, 36, 43, 95, 62, 15, 12]
// ss = '55743748'
// poses= [[50,30, 70, 110], [60, 30, 70, 50], [80, 30, 90, 50]]

// w = get_w(poses, pic, gt, challenge, cc, ss)
// console.log(w)
