//<<<<<<<<<<<<<<<<<<<<<<<mask 
		function checkSpace(str) { 
			if(str.search(/\s/) != -1) { 
				return true; 
			} else { 
				return false; 
			} 
		}
		function checkSpecial(str) {
			var special_pattern = /[`~!@#$%^&*|\\\'\";:\/?]/gi;
			if(special_pattern.test(str) == true) {
				return true;
			} else {
				return false;
			}
		}

		function checkPasswordPattern(str) {
			var pattern1 = /[0-9]/; // 숫자
			var pattern2 = /[a-zA-Z]/; // 문자
			var pattern3 = /[~!@#$%^&*()_+|<>?:{}]/; // 특수문자
			if(!pattern1.test(str) || !pattern2.test(str) || !pattern3.test(str) || str.length < 8) {
				return false;
			} else {
					return true;
			}
		}
		function email_mask(email){
			var regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
			if(email.match(regExp) != null){
				return true
			}
			else{
				return false
			}
		}
		function str_cmp(str1, str2){
			if(str1 == str2){
				return true;
			}else{
				return false;
			}
		}
		
		function checkphoneNum(num){
			var cellExp =  /^[0-9]+$/;
			if(!cellExp.test(num)){
				return true
			}
			else{
				return false
			}
		}
		//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>