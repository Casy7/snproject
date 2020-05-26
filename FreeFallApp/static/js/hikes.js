// function mode(array) {
//     if (array.length == 0)
//         return null;
//     var modeMap = {};
//     var maxEl = array[0], maxCount = 1;
//     for (var i = 0; i < array.length; i++) {
//         var el = array[i];
//         if (modeMap[el] == null)
//             modeMap[el] = 1;
//         else
//             modeMap[el]++;
//         if (modeMap[el] > maxCount) {
//             maxEl = el;
//             maxCount = modeMap[el];
//         }
//     }
//     return maxEl;
// }
// list = [];
// Object.values(document.getElementsByClassName('hike_card')).forEach(tr => {
//     list.push(tr.clientWidth);
// })
// console.log(list)

// most_common_width = Math.max.apply(Math, list);

// Object.values(document.getElementsByClassName('hike_card')).forEach(tr => {
//     if (tr.clientWidth <= most_common_width - 2) {
//         tr.children[0].children[0].children[0].style.width = most_common_width + 'px';
//     }
// })
// document.addEventListener('resize', function ds(){
// list = [];
// Object.values(document.getElementsByClassName('hike_card')).forEach(tr => {
//     list.push(tr.clientWidth);
// })
// console.log(list)

// most_common_width = mode(list);

// Object.values(document.getElementsByClassName('hike_card')).forEach(tr => {
//     if (tr.clientWidth <= most_common_width - 2 || tr.clientWidth >= most_common_width + 2) {
//         tr.children[0].children[0].children[0].style.width = most_common_width + 'px';
//     }
// })
// })