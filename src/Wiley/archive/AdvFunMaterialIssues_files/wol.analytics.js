(function(a,d,f){var b=function(h){for(var g in h){if(h.hasOwnProperty(g)){s[g]=h[g]
}}};
var e=function(h){s.linkTrackEvents="";
s.linkTrackVars="";
var g;
for(g in h){if(h.hasOwnProperty(g)){if(h[g]===f){delete s[g]
}else{s[g]=h[g]
}}}h=({})
};
var c=function(j,l){if(window.s&&window.s.tl){var x=j.jquery?j:d(j),h=x.attr("href")||"",n=x.attr("data-t-sc")||"",t=n?JSON.parse(n.replace(/'/g,'"')):{},g=(l&&l.linkType)?l.linkType:t.linkType||"o",u=(l&&l.linkDesc)?l.linkDesc:t.linkDesc||x.text(),m=(l&&l.linkTrackVars)?l.linkTrackVars:t.linkTrackVars||s.linkTrackVars,r=(l&&l.linkTrackEvents)?l.linkTrackEvents:t.linkTrackEvents||s.linkTrackEvents,w=(l&&l.events)?l.events:t.events,k=(l&&l.eVars)?l.eVars:t.eVars||"",o=(l&&l.sProps)?l.sProps:t.sProps||"",q=[];
s.linkTrackVars=m;
s.linkTrackEvents=r;
s.events=w?s.apl(s.events,w,",",1):s.events;
if(k){b(k)
}var i,v=Object({});
if(o){for(i in o){if(o.hasOwnProperty(i)){v[i]=s[i]
}}b(o)
}s.tl(h,g,u);
e(v);
v=({})
}};
a.analytics={trackLink:c};
return a
}(window.wol=window.wol||{},jQuery));
$(function(){if(window.s){$("body").delegate(".track-click","click",function(){wol.analytics.trackLink(this)
})
}});