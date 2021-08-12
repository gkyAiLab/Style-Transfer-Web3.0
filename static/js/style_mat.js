 $(document).ready(function() {
    window.addEventListener('load',function(){
      var div = document.querySelector('div');
      window.addEventListener('resize', function() {
        console.log(window.innerWidth);
        if (window.innerWidth <=990){
          div.style.display = 'none';
          console.log('change')
        } else {
          div.style.display = 'block';
        }
      })
    })

    // 使程序暂停一段时间
    function sleep(milliSeconds) {
    var startTime = new Date().getTime();
    while (new Date().getTime() < startTime + milliSeconds) {
      console.log(new Date().getTime());
    } 
    }


    $('button').on('click', function() {
      // 如果发现是摄像头开启按钮 
      if ($(this).attr("id").toString() == 'webcam') {
        var withOpenWebcam = '';
        if (document.getElementById("webcam").innerHTML == 'Open Webcam') {
          withOpenWebcam = 'True';
          document.getElementById("webcam").innerHTML = 'Close Webcam';
          // change url{{}}  open camera stream
          document.getElementById("stream").src = "webcam_stream"; 
          // load init model 

        }
        else {
          withOpenWebcam = 'False';
          document.getElementById('webcam').innerHTML = 'Open Webcam';
          document.getElementById("stream").src = "static/images/sunflower.jpg";
          
          // window.location.href = "{{ url_for('style_transfer') }}";
        }

        var changeModel = 'False';
        var withTransferStyle = 'False';
        req = $.ajax({
            url : '/update',
            type : 'POST',
            data: { 
              with_webcam : withOpenWebcam,
              with_style : withTransferStyle, 
              change_model : changeModel, 
              // self.net update 

            }
        });
        req.done(function(data){
        });
      } 
 

       // 抠图的初始化按钮与信号
      if ( $(this).attr("id").toString() == 'startMatting') {
        var withMattingInit = '';  // 抠图的信号 负责初始化一次

        $.getJSON('/update_flask_state', function(data) {
          var withWebcam = data.with_webcam.toString();  // 检查webcam的状态
          
          if (withWebcam != "True"){
            // 如何摄像头还没有打开，提醒用户打开摄像头
            alert("Please open webcam !!")
          } else {
            if (document.getElementById('startMatting').innerHTML != "Restart Matting") {
              document.getElementById('startMatting').innerHTML = 'Restart Matting';
              withMattingInit = 'True';
            } else {
              document.getElementById('startMatting').innerHTML = 'Init Matting';
              withMattingInit = 'False';
              
            }
            // 将抠图的初始化信号给后端
            req = $.ajax({
              url : '/update',
              type : 'POST',
              data: { 
                matting_init : withMattingInit }  
              });
            req.done(function(data){});
          }
        });

      } 
      
      if ($(this).attr("id").toString() == 'Display_QR_code') {
        
        $.getJSON('/update_flask_state', function(data) {
          var videoComplete = data.video_complete.toString();

          if (videoComplete == "True") {
            alert('Video Complete!');
            document.getElementById("qrcode").src = 'static/qrcode/qrcode_out.png';
            $("#qrcode").src = 'static/qrcode/qrcode_out.png';
          } else {
            alert('Please record First !');
          }

        });
      } 

    if ($(this).attr("class").toString() == "style_mode"){
      // } else {
        // 如果点击的是风格迁移按钮
        // 点击其余供能之前应该检查是否打开了摄像头
        // 从后端提取状态信息
        var withTransferStyle = 'True';
        var transferStyle = $(this).attr("id").toString();
        var changeModel = 'True';

        $.getJSON('/update_flask_state', function(data) {
          var withWebcam = data.with_webcam.toString();  // 检查webcam的状态
          if (withWebcam != "True"){
            // 摄像头还没有打开，提醒用户打开摄像头
            alert("Please open webcam !!")
          } else {
            req = $.ajax({
              url : '/update',
              type : 'POST',
              data: { 
                with_style : withTransferStyle, //是否使用风格迁移
                change_model : changeModel,  //change_style_model 风格迁移模型是否改变
                transfer_style : transferStyle //id route
              }  
              });
            req.done(function(data){});
          }
        });
      }

    if ($(this).attr("class").toString() == "matting_mode"){
          // 如果点击的是matting按钮
          // 点击其余供能之前应该检查是否打开了摄像头
          // 从后端提取状态信息
          var withmatting = 'True';
          var input_model = $(this).attr("id").toString() //video img style include (self.stat_mat='3' self.input='style')
          
          //console.log("&&&&&&&&&&&&&&&&&&&",document.getElementById("demo_img").src)
          var changeModel = 'True';
  
          $.getJSON('/update_flask_state', function(data) {
            var withWebcam = data.with_webcam.toString();  // 检查webcam的状态
            if (withWebcam != "True"){
              // 摄像头还没有打开，提醒用户打开摄像头
              alert("Please open webcam !!")
            } else {
              req = $.ajax({
                url : '/update',
                type : 'POST',
                data: { 
                  with_matting : withmatting, //是否使用matting
                  change_model : changeModel,  //change_style_model 风格迁移模型是否改变
                  input_model : input_model //id route (self.stat_mat self.input)
                }  
                });
              req.done(function(data){});
            }
          });
        }

    if ($(this).attr("id").toString() == "0"){
          // 如果点击的是no matting按钮
          // 点击其余供能之前应该检查是否打开了摄像头
          // 从后端提取状态信息
          
          var withmatting = 'False';
          var withTransferStyle='False';
          var input_model = $(this).attr("id").toString() //video img style include (self.stat_mat='3' self.input='style')
          
          var changeModel = 'True';
          // var sytle_model = 'None';
  
          $.getJSON('/update_flask_state', function(data) {
            var withWebcam = data.with_webcam.toString();  // 检查webcam的状态
            if (withWebcam != "True"){
              // 摄像头还没有打开，提醒用户打开摄像头
              alert("Please open webcam !!")
            } else {
              req = $.ajax({
                url : '/update',
                type : 'POST',
                data: { 
                  with_matting : withmatting, //是否使用matting
                  with_style: withTransferStyle, 
                  change_model : changeModel,  //change_style_model 风格迁移模型是否改变
                  input_model : input_model, //id route (self.stat_mat self.input)
                  // sytle_model:sytle_model
                }  
                });
              req.done(function(data){});
            }
          });
        }
      
    if ($(this).attr("id").toString() == "init_cam"){
      // 如果点击的是no matting按钮
      // 点击其余供能之前应该检查是否打开了摄像头
      // 从后端提取状态信息
      var style_init_down='True';

      $.getJSON('/update_flask_state', function(data) {
        var withWebcam = data.with_webcam.toString();  // 检查webcam的状态
        if (withWebcam != "True"){
          // 摄像头还没有打开，提醒用户打开摄像头
          alert("Please open webcam !!")
        } else {
          req = $.ajax({
            url : '/update',
            type : 'POST',
            data: { 
              style_init_down:style_init_down,
            }  
            });
          req.done(function(data){});
        }
      });
    }
    if ($(this).attr("id").toString() == "recordButton"){
      $.getJSON("/update_flask_state", function(data) {
        var withWebcam = data.with_webcam.toString();  // 检查webcam的状态
  
        if (withWebcam != "True") {
          alert("Please open webcam !!")
        } else {
          var withRecord = '';
          var startVideoComplete = '';
          var videoComplete = '';
  
          if (document.getElementById("recordButton").innerHTML == '<i class="layui-icon layui-icon-play" style="font-size: 20px;"></i>录制开始') {
            withRecord = 'True';
            startVideoComplete = 'False';
            videoComplete = 'False';
            document.getElementById("recordButton").innerHTML = '正在录制';
          } else {
            withRecord = 'False';
            startVideoComplete = 'True';
            document.getElementById('recordButton').innerHTML = '<i class="layui-icon layui-icon-play" style="font-size: 20px;"></i>录制开始';
            VideoComplete = 'False';
          }
  
          // 检查没有问题，开始传输录制信号
          req = $.ajax({
            url : '/update',
            type : 'POST',
            data: { with_record : withRecord, video_complete : videoComplete ,start_video_complete : startVideoComplete}
          });
          req.done(function(data){ });
        }
      });
    }
    if ($(this).attr("id").toString() == "takePictures"){
      $.getJSON('/update_flask_state', function(data) {
        var withWebcam = data.with_webcam.toString(); 
        if (withWebcam != 'True') {
          alert('Please open webcam !!')
        } else {
          var withTakePictures = 'True';
          req = $.ajax({
            url : '/update',
            type : 'POST',
            data: { 
              with_take_pictures : withTakePictures }  
          });
          req.done(function(data) {});
        }
    
        if (withWebcam == 'True') {
          sleep(500);
    
          // 信号给出后，紧接着检查后台数据是否完成，
          layer.alert('<button type="button" id="printPhoto" class="layui-btn layui-btn-normal">打印</button><br>此处放二维码图片，请扫码观看下载。<br><img id="photo" style="height: 10%; width: 30%;" class="layui-anim layui-anim-scale"><img id = "photoQrcode" style="height: 150px; width: 150px;" class="layui-anim layui-anim-scale">', {
              time: 30*1000
              ,success: function(layero, index){
                document.getElementById('photo').src = 'static/picture/picture.png?' + Math.random();
                document.getElementById('photoQrcode').src = 'static/qrcode/qrcode.png?' + Math.random();
                var timeNum = this.time/1000, setText = function(start){
                  layer.title((start ? timeNum : --timeNum) + ' 秒后关闭', index);
                };
                setText(!0);
                this.timer = setInterval(setText, 1000);
                if(timeNum <= 0) clearInterval(this.timer);
              
              // 传递打印的信号
              $("#printPhoto").on("click", function() {
                var printPhoto = 'True'; 
                req = $.ajax({
                  url : '/update',
                  type : 'POST',
                  data: { 
                    print_photo : printPhoto}  
                });
                req.done(function(data) {});
              });  
    
              }
              ,end: function(){
                clearInterval(this.timer);
              }    
          });
        }
      }); 

    }
    if ($(this).attr("id").toString() == "viewVideo"){
      $.getJSON("/update_flask_state", function(data) {
        var videoComplete = data.video_complete.toString();
        if (videoComplete == 'False') {
          alert("暂时没有合成的视频...")
        } else {
          layer.alert('<br>此处放二维码图片，请扫码观看下载。<br><img id = "videoQrcode" style="height: 150px; width: 150px;" class="layui-anim layui-anim-scale">', {
              time: 30*1000
              ,success: function(layero, index){
                document.getElementById('videoQrcode').src = 'static/qrcode/qrcode_out.png?' + Math.random();
                var timeNum = this.time/1000, setText = function(start){
                  layer.title((start ? timeNum : --timeNum) + ' 秒后关闭', index);
                };
                setText(!0);
                this.timer = setInterval(setText, 1000);
                if(timeNum <= 0) clearInterval(this.timer);
              }
              ,end: function(){
                  clearInterval(this.timer);
              }    
          });
        }
      })
    }

      
    });
  });

