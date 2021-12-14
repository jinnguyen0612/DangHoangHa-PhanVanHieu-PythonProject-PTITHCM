var currentQuestion = 0;
var viewingAns = 0;
var correctAnswers = 0;
var quizOver = false;
var iSelectedAnswer = [];
var c = time*60;
var t;
$(document).ready(function ()
{
    // Display the first question
    displayCurrentQuestion();
    $(document).find(".submit_btn").hide();
	$(document).find(".end_btn").hide();
    $(this).find(".quizMessage").hide();
    $(this).find(".preButton").attr('disabled', 'disabled');

	timedCount();

	$(this).find(".preButton").on("click", function ()
	{

        if (!quizOver)
		{
			if(currentQuestion == 0) {
                return false;
            }

			if(currentQuestion == 1) {
			  $(".preButton").attr('disabled', 'disabled');
			  $(document).find(".nextButton").text("Next Question");
			}
				currentQuestion--;// Since we have already displayed the first question on DOM ready
				displayCurrentQuestion();
		} else {
			if(viewingAns == 3) { return false; }
			currentQuestion = 0; viewingAns = 3;
			viewResults();
		}
    });


	// On clicking next, display the next question
    $(this).find(".nextButton").on("click", function ()
	{
        if (!quizOver)
		{
            var val = $("input[type='radio']:checked").val();

            if (val == undefined)
			{
                $(document).find(".quizMessage").text("Please select an answer");
                $(document).find(".quizMessage").show();
            }
			else
			{
                // TODO: Remove any message -> not sure if this is efficient to call this each time....
                $(document).find(".quizMessage").hide();
				if (val == questions[currentQuestion].correctAnswer)
				{
					correctAnswers++;
				}
//				iSelectedAnswer[currentQuestion] = val;
				 currentQuestion++;
				 // Since we have already displayed the first question on DOM ready
				if(currentQuestion >= 1) {
					  $('.preButton').prop("disabled", false);
      				  $(document).find(".nextButton").text("Next Question");
				}
				if (currentQuestion < questions.length)
				{
					displayCurrentQuestion();

				}
				else
				{
                    document.getElementById('selected').value = iSelectedAnswer.toString();
				    document.getElementById('my_score').value = (100/questions.length)*correctAnswers ;
				    $(document).find(".submit_btn").show();
				    currentQuestion = questions.length - 1;
				}
			}
		}
    });


   $(document).find(".submit_btn").on("click", function (){
     Unread();
   });
});

var URL="/results/";
function Unread(){

        var data = {'selected': iSelectedAnswer, 'X-csrfmiddlewaretoken': csrfmiddlewaretoken};
        $.post(URL, data);

 }

function timedCount()
	{
		if(c == 185)
		{
			return false;
		}
		var hours = parseInt( c / 3600 ) % 24;
		var minutes = parseInt( c / 60 ) % 60;
		var seconds = c % 60;
		var result = (hours < 10 ? "0" + hours : hours) + ":" + (minutes < 10 ? "0" + minutes : minutes) + ":" + (seconds  < 10 ? "0" + seconds : seconds);
		$('#timer').html(result);

		if(c == 0 )
		{
		    $(document).find(".submit_btn").show();
		    $(document).find(".submit_btn").on("click", function (){
             Unread();
           });
            document.getElementById('selected').value = iSelectedAnswer.toString();
            document.getElementById("submit_btn").click();
           $(document).find(".nextButton").text("Next Question").hide();
           $(document).find(".preButton").text("Next Question").hide();
           return false;
		}
		c = c - 1;
		t = setTimeout(function()
		{
			timedCount()
		},1000);
	}

// This displays the current question AND the choices
function displayCurrentQuestion()
{
	if(c == 185) { c = 180; timedCount(); }
    //console.log("In display current Question");
    var question = "Question " + (currentQuestion+1) +": " + questions[currentQuestion].question;
    var questionClass = $(document).find(".quizContainer > .question");
    var choiceList = $(document).find(".quizContainer > .choiceList");
    var numChoices = questions[currentQuestion].choices.length;
    // Set the questionClass text to the current question
    $(questionClass).text(question);
    // Remove all current <li> elements (if any)
    $(choiceList).find("li").remove();
    var choice;
    $(document).on('click', 'input[name="dynradio"]', function() {
        iSelectedAnswer[currentQuestion] = $(this).val();

    });
    for (i = 0; i < numChoices; i++)
	{
        choice = questions[currentQuestion].choices[i];

		if(iSelectedAnswer[currentQuestion] == i) {

			$('<li><input type="radio" class="radio-inline" checked="checked"  value=' + i + ' name="dynradio" />' +  ' ' + choice  + '</li>').appendTo(choiceList);
		} else {
			$('<li><input type="radio" class="radio-inline" value=' + i + ' name="dynradio" />' +  ' ' + choice  + '</li>').appendTo(choiceList);
		}
    }
}