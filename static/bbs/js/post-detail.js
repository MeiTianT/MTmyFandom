
$(function () {



    //个人资料修改密码
    $('#jsPoVideo').on('click', function(){
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    }); 5

    $('#jsResetPwdBtn').click(function(){
        $.ajax({
            cache: false,
            type: "POST",
            dataType:'json',
            url:"/users/update/pwd/",
            data:$('#jsResetPwdForm').serialize(),
            async: true,
            success: function(data) {
                if(data.password1){
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                }else if(data.password2){
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title:'提交成功',
                        h2:'修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                }else if(data.msg){
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });








    // 获取弹窗
    modal = document.getElementById('myModal');

    // 获取 <span> 元素，用于关闭弹窗
    span = document.querySelector('.close');

    // 点击 <span> (x), 关闭弹窗
    span.onclick = function() {
            modal.style.display = "none";
        }

    // 在用户点击其他地方时，关闭弹窗
    window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

    //获取评论id
    function reply(obj){
        pnode = obj.parentNode.parentNode;
        replyId = pnode.id
        //console.log(replyId)
        return replyId
    }
    //构造url
    $('.reply').click(function () {
        var c='/users/reply/comment/'
        var id=reply(this)
        //console.log(typeof(id)) string
        //id=Number(id)
        reply_url=c+id+'/'

        // 点击按钮打开弹窗
         modal.style.display = "block";
        })


    //回复评论
    $('#reply-form').submit(function (event) {
        var new_reply = $(event.target).find('textarea').val();
        console.log(reply_url) //这里能获取到url /users/reply/comment/45/

        var url=reply_url

        $.ajax({
            type: "post",
            url: url,
            data: {"new_reply":new_reply,"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
            //dataType: 'json',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(){
                        //$('#reply-form')[0].reset();
                        alert("回复成功"); //成功时弹出view传回来的结果
                        window.location.reload();//刷新当前页面.
                        //Dml.fun.winReload();

                    },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });

    //发布评论
    $('#po-comment-form').submit(function (event) {
        var url = $(event.target).attr('action');
        var comment_content = $(event.target).find('textarea').val();
        //提交验证
        if (comment_content == null || comment_content == '') {
            var warn_element = $(event.target).find('.warning');
            warn_element.css('display', 'inline-block');
            var warn_text_element = warn_element.find('.warning-text');
            warn_text_element.text('请输入评论内容');
            return false;
        }

        console.log(url)
        $.ajax({
            type: "post",
            url: url,
            data: {
                "comment": comment_content,"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()
            },
            //dataType: 'json',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(data){
                        $('#po-comment-form')[0].reset();
                        alert("发布成功"); //成功时弹出view传回来的结果
                        window.location.reload();//刷新当前页面.
                        //Dml.fun.winReload();
                    },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });

    //发布帖子
    $('#po-article-form').submit(function (event) {
        var url = $(event.target).attr('action');
        var article_content = $(event.target).find('textarea').val();
        //提交验证
        if (comment_content == null || comment_content == '') {
            var warn_element = $(event.target).find('.warning');
            warn_element.css('display', 'inline-block');
            var warn_text_element = warn_element.find('.warning-text');
            warn_text_element.text('请输入评论内容');
            return false;
        }


        $.ajax({
            type: "post",
            url: url,
            data:$("po-article-form").serialize(),
            dataType: 'json',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(result){
                        //$('#po-article-form')[0].reset();
                        alert(result); //成功时弹出view传回来的结果
                    },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });

    //发布图片
    $('#po-picture-form').submit(function (event) {
        var url = $(event.target).attr('action');
        $.ajax({
            type: "post",
            url: url,
            data: $("po-picture-form").serialize(),
            dataType: 'json',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(result){
                        //$('#po-picture-form')[0].reset();
                        alert(data.status); //成功时弹出view传回来的结果
                    },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });

    //发布视频
    $('#po-video-form').submit(function (event) {
        var url = $(event.target).attr('action');
        $.ajax({
            type: "post",
            url: url,
            data: $("po-video-form").serialize(),
            dataType: 'json',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function(result){
                        $('#po-video-form')[0].reset();
                        alert(data.status); //成功时弹出view传回来的结果
                    },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });











    $('.delete').on('click', function (event) {
        deleteEvent(event);
    });

    function deleteEvent(event) {
        if (confirm("确认删除?")) {
            var comment_id = $(event.target).attr('data-id');
            $.ajax({
                type: "post",
                url: "/comment/delete/" + comment_id,
                data: {},
                dataType: 'json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                },
                success: function (data) {
                    var delete_comment_id = 'comment-' + data.comment_id;
                    var delete_element = $('#' + delete_comment_id);
                    var parent_div = delete_element.parent('.child-comment-list');
                    delete_element.remove();
                    /*
                     * 查看父节点是否为Div，若为Div，则证明删除元素为楼中楼评论，
                     * 在查看父Div下是否有其他Div元素，若没有，则证明再无楼中楼评论
                     * 可直接删除父Div
                     */
                    if (parent_div.is('div')) {
                        var has_children = parent_div.find('div').length > 2;
                        if (!has_children) {
                            parent_div.addClass('hide')
                        }
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    console.log(XMLHttpRequest.responseText);
                }
            });
        }
    }

    $('.reply').on('click', function (event) {
        replyEvent(event);
    });

    function replyEvent(event) {
        var current_tag = $(event.target);
        var target_username = current_tag.attr('data-nickname');
        var root_id = current_tag.attr('data-id');
        var parent_id = current_tag.attr('data-id');
        //找出form展示出来
        var form_parent_element = current_tag.parents('.blog-comment-content').find('.child-comment-list');
        form_parent_element.removeClass('hide');
        var form_element = form_parent_element.find('form');
        form_element.css('display', 'block');
        //找到form中的input[name=root_id] 和 input[name=parent_id]项，赋予root_id 和 parent_id给它
        form_element.find('input[name=root_id]').val(root_id);
        form_element.find('input[name=parent_id]').val(parent_id);
        //再找出form中的textarea，把@赋予它
        form_element.find('textarea').val('@' + target_username + ' ').focus();
    }

    $('.child_reply').on('click', function (event) {
        childReplyEvent(event);
    });

    function childReplyEvent(event) {
        var current_tag = $(event.target);
        var target_username = current_tag.attr('data-nickname');
        var root_id = current_tag.attr('data-root-id');
        var parent_id = current_tag.attr('data-parent-id');
        //找出form展示出来
        var form_element = current_tag.parents('.child-comment-list').find('form');
        form_element.css('display', 'block');
        //找到form中的input[name=root_id] 和 input[name=parent_id]项，赋予root_id 和 parent_id给它
        form_element.find('input[name=root_id]').val(root_id);
        form_element.find('input[name=parent_id]').val(parent_id);
        //再找出form中的textarea，把@赋予它
        form_element.find('textarea').val('@' + target_username + ' ').focus();
    }

    $('.child-comment-form').submit(function (event) {
        return child_commment_form_submit(event)
    });

    function child_commment_form_submit(event) {
        var current_tag = $(event.target)
        var url = current_tag.attr('action');
        var comment_content = current_tag.find('textarea').val();
        var root_id = current_tag.find('input[name=root_id]').val();
        var parent_id = current_tag.find('input[name=parent_id]').val();
        //提交验证
        if (comment_content == null || comment_content == '') {
            var warn_element = $(event.target).find('.warning');
            warn_element.css('display', 'inline-block');
            var warn_text_element = warn_element.find('.warning-text');
            warn_text_element.text('请输入评论内容');
            return false;
        }
        $.ajax({
            type: "post",
            url: url,
            data: {
                "comment": comment_content,
                "root_id": root_id,
                "parent_id": parent_id
            },
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (data, textStatus) {
                current_tag.css('display', 'none');
                //组装html
                var comment_html = '<div class="child-comment" id="comment-' + data.comment_id + '">';
                comment_html += '<p><a class="blue-link" href="#">' + data.comment_author + '</a>：' + data.comment_content + '</p>';
                comment_html += '<div class="child-comment-footer text-right clearfix">';
                if (data.user_id == data.author_id) {
                    comment_html += '<a data-id="' + data.comment_id + '" class="delete" href="javascript:void(0)">删除</a> ';
                }
                comment_html += '<a data-parent-id="' + data.comment_id + '" data-root-id="' + root_id + '" data-nickname="' + data.comment_author + '" class="child_reply" href="javascript:void(0)">回复</a>';
                comment_html += '<span class="reply-time pull-left">' + data.comment_publish_time + '</span>';
                comment_html += '</div></div>';

                //判断是否有子评论
                if (current_tag.parent('.child-comment-list').find('.child-comment').length > 0) {
                    var last_comment_element = current_tag.parent('.child-comment-list').find('.child-comment').last();
                    last_comment_element.after(comment_html);
                } else {
                    current_tag.parent('.child-comment-list').prepend(comment_html);
                }

                var new_comment_element = current_tag.parent('.child-comment-list').find('.child-comment').last();
                new_comment_element.on('click', '.delete', function (event) {
                    deleteEvent(event);
                });
                new_comment_element.on('click', '.child_reply', function (event) {
                    childReplyEvent(event);
                });
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    }

});
