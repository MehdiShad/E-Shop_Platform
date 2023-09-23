function sensArticleComment(articleId) {
    console.log("hello")
    let comment = $('#commentText').val()
    let parentId = $('#parent_id').val()
    console.log("parentId", parentId)
    //ajax => asynchronous javascripts and xml
    //json => javascripts object notation
    $.get('/articles/add-article-comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId,
    }).then(res => {
        console.log(res)
        // location.reload() // رفرش کردن صفحه
        $('#comments_area').html(res)
        $('#commentText').val('') //خالی کزدن مقدار بعد از ثبت
        $('#parent_id').val('') //خالی کزدن مقدار بعد از ثبت
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"})
        } else {
            document.getElementById('comments_area').scrollIntoView({behavior: "smooth"})
        }

    })
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId)
    // window.scrollTo()
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"})
}