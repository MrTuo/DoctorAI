
$(document).ready(function() { 

  function getNumberInNormalDistribution(mean, std_dev){    
     return mean + (uniform2NormalDistribution() * std_dev);
  }

  function uniform2NormalDistribution(){
    var sum = 0.0;
    for(var i = 0; i < 12; i++) {
      sum = sum + Math.random();
    }
    return sum - 6.0;
  }

  function obfuscation() {
    var fields = $('[type=number]').serializeArray();
    $.each(fields, function(i, filed) {
      var temp = Number(this.value) + getNumberInNormalDistribution(0.5, 0.1);
      this.value = temp.toString();
      // console.log(this);
    });
  }

 
  $(window).scroll(function() {
	  var value = $(this).scrollTop();
      if (value > 0)
        $(".my-navbar").css("background-color", "#fff").css("transition-duration", ".4s");
      else {
        $(".my-navbar").css("background-color", "transparent");
      }
  });
  
  function centerModals() {
	  $('.modal').each(function(i){   //遍历每一个模态框
	       var $clone = $(this).clone().css('display', 'block').appendTo('body');    
	       var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
	       top = top > 0 ? top : 0;
	       $clone.remove();
	       $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
	   });
	  var paddingRightLen = -(window.innerWidth - document.documentElement.clientWidth);
	  $("body").css("padding-right", paddingRightLen);		//解决
	  $("body").css("overflow-y", "hidden");
  }

  $(".modal").on("show.bs.modal", centerModals);      //当模态框出现的时候
  $(".modal").on("hide.bs.modal", function() {
  	$("body").css("padding-right", "0px");
  	$("body").css("overflow-y", "auto");
    $("#sign-result").html("");
  	$("#email").val("");
  	$("#Password").val("");
  });


});

