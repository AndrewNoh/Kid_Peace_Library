		var idCheck = 0;	//id 중복검사 확인 변수
		var passCheck = 0; //패스워드 검사 확인 변수
		var emailCheck = 0; // email 확인 변수
		var phoneNumCheck = 0;
		

//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< signup function
		
		//회원가입 핸드폰번호 검사
		function signup_checkphoneNum(){
			input_cell = $('#cell_phone').val()
			if(input_cell ==''){
				alert('전화번호를 입력하세요!')
				$('#cell_phone').focus()
				 return false;
			}else if(checkphoneNum(input_cell)){
				alert("잘못된 전화번호입니다. 숫자만 입력하세요.");
				$('#cell_phone').focus()
				$('#cell_phone').select()
				return false;
			}
			return true;
		}
		
		//폼 초기화 
		function signup_clearForm(){
			$('#id').val(null)
			$('#password').val(null)
			$('#rpassword').val(null)
			$('#email').val(null)
			$('#name').val(null)
			$('#cell_phone').val(null)
			$('#sign_up_btn').prop("disabled", true);
			$('#id').css("background-color", "#FFCECE");
			$('#rpassword').css("background-color", "#FFCECE");
			$('#email').css("background-color", "#FFCECE");
			$('#cell_phone').css("background-color", "#FFCECE");
		}
		
		//회원가입 email 검사
		function signup_checkEmail(){
			 var input_email = $('#email').val();
			 if(email_mask(input_email)){
				$('#email').css("background-color", "#B0F6AC");
				emailCheck = 1;
				if(idCheck == 1 && passCheck == 1 && emailCheck == 1){
					$('#sign_up_btn').prop("disabled", false);
					$('#sign_up_btn').css("background-color", "#4CAF50");
				}
			 }else{
				 $('#email').css("background-color", "#FFCECE");
			 }
		}

		//회원가입 비밀번호 재입력 검
		function signup_repeatPassword(){
			var input_password = $('#password').val();
			var input_rpassword = $('#rpassword').val();

			if(str_cmp(input_password,input_rpassword)){
				$('#rpassword').css("background-color", "#B0F6AC");
				passCheck = 1;
				if(idCheck == 1 && passCheck == 1 && emailCheck == 1){
					$('#sign_up_btn').prop("disabled", false);
					$('#sign_up_btn').css("background-color", "#4CAF50");
				}
			}else{
				$('#rpassword').css("background-color", "#FFCECE");
			}
		}

		//회원가입 비밀번호 특수문자, 자리수, 숫자 검사
		function signup_checkPassword(){
			if(checkPasswordPattern($('#password').val())){
				$('#password').css("background-color", "#B0F6AC");
				return true;
			}
			else{
				alert("회원가입 실패! 비밀번호는 8자리 이상 문자, 숫자, 특수문자로 구성하여야 합니다.")
				$('#password').val('');
				$('#password').focus();
				$('#rpassword').css("background-color", "#FFCECE");
				$('#sign_up_btn').prop("disabled", true);
				passCheck = 0;
				return false;
			}
		}
		
		//id 중복 검사 ajax
		function checkId(){
			var input_id = $('#id').val();
			$.getJSON($SCRIPT_ROOT + '/user/check_id', {
					id: input_id
				}, function(data) {
					if($.trim(data.count) == 0 && (input_id == null || input_id=='')){
						$('#sign_up_btn').prop("disabled", true);
						$('#id').css("background-color", "#FFCECE");
						$('#checkMsg').html('<p class="text-danger" style="margin-top:-15px; margin-bottom:-20px">사용 불가능</p>');
						idCheck = 0;
					}
					else if($.trim(data.count) == 0 && checkSpace(input_id)){
						$('#sign_up_btn').prop("disabled", true);
						$('#id').css("background-color", "#FFCECE");
						$('#checkMsg').html('<p class="text-danger" style="margin-top:-15px; margin-bottom:-20px">공백 사용 불가능</p>');
						idCheck = 0;
					}
					else if($.trim(data.count) == 0 && checkSpecial(input_id)){
						$('#sign_up_btn').prop("disabled", true);
						$('#id').css("background-color", "#FFCECE");
						$('#checkMsg').html('<p class="text-danger" style="margin-top:-15px; margin-bottom:-20px">특수문자 사용 불가능</p>');
						idCheck = 0;
					}
					else if($.trim(data.count) == 0){
							$('#id').css("background-color", "#B0F6AC");
							$('#checkMsg').html('<p class="text-success" style="margin-top:-15px; margin-bottom:-20px">사용 가능</p>');
							idCheck = 1;
							if(idCheck == 1 && passCheck == 1 && emailCheck == 1){
								$('#sign_up_btn').prop("disabled", false);
								$('#sign_up_btn').css("background-color", "#4CAF50");
							}
					}
					else if($.trim(data.count) == 1){
						$('#id').css("background-color", "#FFCECE");
						$('#checkMsg').html('<p class="text-danger" style="margin-top:-15px; margin-bottom:-20px">사용 불가능</p>');
						$('#sign_up_btn').prop("disabled", true);
						idCheck = 0;
					}
			});
		}
		
		//회원가입 ajax
		$(function() {
		    $('#sign_up_btn').click(function() {
		    	if(!signup_checkPassword())
		    		return;
		    	if(!signup_checkphoneNum())
		    		return;
		        var id = $('#id').val();
		        var password = $('#password').val();
		        var email = $('#email').val();
		        var name = $('#name').val();
		        var cell_phone = $('#cell_phone').val();
		        $.ajax({
		            url: '/user/Signup',
		            data: $('form').serialize(),
		            type: 'POST',
		            success: function(data) {
		                status = $.trim(data.status);
		                if(status == 'error'){
		                	alert('회원가입 실패')
		                }else if(status == 'ok'){
		                	signup_clearForm()
		                	alert('가입 완료')
		                }
		            },
		            error: function(error) {
		                console.log(error);
		            }
		        });
		    });
		});
		//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>