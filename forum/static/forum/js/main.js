/*Counter Animation*/
// let nCount = function (selector) {
//     $(selector).each(function () {
//         $(this).animate({
//             Counter: $(this).text()
//         }, {
//             duration: 4000,
//             easing: "swing",
//             step: function (value) {
//                 $(this).text(Math.ceil(value));
//             }
//         });
//     });
// };

// let a = 0;
// $(window).scroll(function () {
//     let oTop = $(".numbers").offset().top - window.innerHeight;
//     if (a == 0 && $(window).scrollTop() >= oTop) {
//         a++;
//         nCount(".rect > h1");
//     }
// })

//Number Counter
$('#numcounterup').counterUp({
    delay: 10,
    time: 1000
});
$('#numcounterup1').counterUp({
    delay: 10,
    time: 1000
});
$('#numcounterup2').counterUp({
    delay: 10,
    time: 1000
});
