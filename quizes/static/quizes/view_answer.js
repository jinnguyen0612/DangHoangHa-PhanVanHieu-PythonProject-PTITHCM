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

				currentQuestion--; // Since we have already displayed the first question on DOM ready
				if (currentQuestion < questions.length)
				{
					displayCurrentQuestion();
					correctAnswers--;

				}
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
				iSelectedAnswer[currentQuestion] = val;

				currentQuestion++; // Since we have already displayed the first question on DOM ready
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
				}
			}

		}
		else
		{

		    // quiz is over and clicked the next button (which now displays 'Play Again?'
			quizOver = false; $('#iTimeShow').html('Time Remaining:'); iSelectedAnswer = [];
			$(document).find(".nextButton").text("Next Question");
			$(document).find(".preButton").text("Previous Question");
			 $(".preButton").attr('disabled', 'disabled');
			resetQuiz();
			viewingAns = 1;
			displayCurrentQuestion();
			hideScore();
		}
    });
   $(document).find(".submit_btn").on("click", function (){
     Unread();
   });

});

var URL="{% url 'quizes:save_result' %}";
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
					displayScore();
					$('#iTimeShow').html('Quiz Time Completed!');
					$('#timer').html("You scored: " + correctAnswers + " out of: " + questions.length);
					c=185;
					$(document).find(".preButton").text("View Answer");
					$(document).find(".nextButton").text("Play Again?");
					quizOver = true;
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

function resetQuiz()
{
    currentQuestion = 0;
    correctAnswers = 0;
    hideScore();
}

function displayScore()
{
    $(document).find(".quizContainer > .result").text("You scored: " + correctAnswers + " out of: " + questions.length);
    $(document).find(".quizContainer > .result").show();
}

function hideScore()
{
    $(document).find(".result").hide();
}

// This displays the current question AND the choices
function viewResults()
{


//	hideScore();
    var question = questions[currentQuestion].question;
    var questionClass = $(document).find(".quizContainer > .question");
    var choiceList = $(document).find(".quizContainer > .choiceList");
    var numChoices = questions[currentQuestion].choices.length;
    // Set the questionClass text to the current question
    $(questionClass).text(question);
    // Remove all current <li> elements (if any)
    $(choiceList).find("li").remove();
    var choice;


	for (i = 0; i < numChoices; i++)
	{
        choice = questions[currentQuestion].choices[i];

		if(iSelectedAnswer[currentQuestion] == i) {
			if(questions[currentQuestion].correctAnswer == i) {
				$('<li style="border:2px solid green;margin-top:10px;"><input type="radio" class="radio-inline" checked="checked"  value=' + i + ' name="dynradio" />' +  ' ' + choice  + '</li>').appendTo(choiceList);
			} else {
				$('<li style="border:2px solid red;margin-top:10px;"><input type="radio" class="radio-inline" checked="checked"  value=' + i + ' name="dynradio" />' +  ' ' + choice  + '</li>').appendTo(choiceList);
			}
		} else {
			if(questions[currentQuestion].correctAnswer == i) {
				$('<li style="border:2px solid green;margin-top:10px;"><input type="radio" class="radio-inline" value=' + i + ' name="dynradio" />' +  ' ' + choice  + '</li>').appendTo(choiceList);
			} else {
				$('<li><input type="radio" class="radio-inline" value=' + i + ' name="dynradio" />' +  ' ' + choice  + '</li>').appendTo(choiceList);
			}
		}
    }

	currentQuestion++;

}

