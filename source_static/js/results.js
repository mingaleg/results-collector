    function repaginate(page) {
        $('.pages').html('')
        $('.pages').append('<a onclick="turn_left();" class="icon item" pg="left">\
                        <i class="left arrow icon"></i>\
                    </a>')
        if (pages > 9) {
            $('.pages').append('<a onclick="turn(1);" class="item" pg="1">1</a>')
            if (page <= 5) {
                for (var i = 2; i <= 7; ++i) {
                    $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a>")
                }
                $('.pages').append('<div class="disabled item">...</div>')
                var i = pages;
                $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a")
                $('.pages').append('<a onclick="turn_right();" class="icon item" pg="right">\
                                <i class="right arrow icon"></i>\
                            </a>')
                return;
            } else if (page + 4 >= pages) {
                $('.pages').append('<div class="disabled item">...</div>')
                for (var i = pages-6; i <= pages; ++i) {
                    $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a>")
                }
                $('.pages').append('<a onclick="turn_right();" class="icon item" pg="right">\
                                <i class="right arrow icon"></i>\
                            </a>')
                return;
            } else {
                $('.pages').append('<div class="disabled item">...</div>')
                for (var i = page-2; i <= page; ++i) {
                    $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a>")
                }
            }
            if (page + 4 >= pages) {
                for (var i = page-3; i <= pages; ++i) {
                    $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a>")
                }
            } else {
                for (var i = page+1; i <= page+2; ++i) {
                    $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a>")
                }
                $('.pages').append('<div class="disabled item">...</div>')
                var i = pages;
                $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a")
            }
            $('.pages').append('<a onclick="turn_right();" class="icon item" pg="right">\
                            <i class="right arrow icon"></i>\
                        </a>')
        } else {
            for (var i = 1; i <= pages; ++i) {
                $('.pages').append('<a onclick="turn(' + i + ');" class="item" pg="'+i+'">' + i + "</a>")
            }
            $('.pages').append('<a onclick="turn_right();" class="icon item" pg="right">\
                            <i class="right arrow icon"></i>\
                        </a>')
        }
    }

    function turn(new_page) {
        $('.content').html('<i class="massive loading icon"></i>')
        repaginate(new_page);
        var href = window.location.href
        if (href.slice(-1) == '/') href=href.slice(0, -1)
        $('.content').load(href + '/page/' + new_page);
        $('.pages .item').removeClass('active')
        $('.pages .item[pg=' + new_page + ']').addClass('active')
        $('.pages .item[pg=left]').removeClass('disabled')
        if (new_page == 1) $('.pages .item[pg=left]').addClass('disabled')
        $('.pages .item[pg=right]').removeClass('disabled')
        if (new_page == pages) $('.pages .item[pg=right]').addClass('disabled')
        page = new_page;
    }

    function turn_left() {
        turn(page-1);
    }

    function turn_right() {
        turn(page+1);
    }

$.ajaxSetup ({
    cache: false
});


$(function() {
    $('.pages').clone().appendTo('.page .segment').addClass('right paginator')
    turn(1);
})

function go_grade(grade) {
    var foo = window.location.href
    if (!grade) {
        foo = foo.replace(/\/grade\/\d+\//g, '/')
        window.location.href = foo
        return
    }
    bar = foo.replace(/\/grade\/\d+\//g, '/grade/' + grade + '/')
    if (foo == bar) {
        foo = foo + 'grade/' + grade
    } else {
        foo = bar
    }
    window.location.href = foo
}