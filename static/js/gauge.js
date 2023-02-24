// function DrawGauge(normalValue,warningValue,dangerValue,currentValue,chartContainer,gaugemeterContainer){
//     var chartcanvas =document.getElementById(chartContainer);
//     var chartwrapper = chartcanvas.parentNode;

//     chartcanvas.setAttribute('width',window.getComputedStyle(chartwrapper).width);
//     chartcanvas.setAttribute('height',window.getComputedStyle(chartwrapper).height);
//     var  ctxchart =chartcanvas.getContext('2d');

//     var myChart =new chartContainer(ctxchart,{
//         type:'doughnt',
//         responsive:true,
//         data:{
//             datasets:[{
//                 backgroundColor:['green','yellow','red'],
//                 data:[normalValue,warningValue,dangerValue]
//             }]
//         },
//         options:{
//             lengend:{
//                 display:false
//             },
//             circumference:Math.PI
//         }
//     });

//     ctxchart.translate(3* chartcanvas.width /8, 3 * chartcanvas.height /8);
//     ctxchart.rotate(3 * Math.PI /2);
//     ctxchart.translate(-3 * chartcanvas .width /8, -3 * chartcanvas,height /8);
// }

