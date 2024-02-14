$(function () {
    $("#carousel-multiple").on("slide.bs.carousel", function (e) {
        var itemsPerSlide = parseInt($(this).attr('data-maximum-items-per-slide')),
        totalItems = $(".carousel-item", this).length,
        reserve = 1,
        $itemsContainer = $(".carousel-inner", this),
        it = (itemsPerSlide + reserve) - (totalItems - e.to);

        if (it > 0) {
        for (var i = 0; i < it; i++) {
            $(".carousel-item", this)
            .eq(e.direction == "left" ? i : 0)
            .appendTo($itemsContainer);
        }
        }
    });
});
$("#carousel-multiple").carousel({
interval: 5000
})