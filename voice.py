import os
import azure.cognitiveservices.speech as speechsdk

#TODO add language selection
def Voice(text):
	speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('AZURE_SPEECH_KEY'), region='eastasia')

	# speech_config.speech_synthesis_voice_name = 'zh-TW-HsiaoYuNeural'
	speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"

	# Check if the directory exists
	if not os.path.exists("./media/voice"):
		# Create a new directory
		os.mkdir("./media/voice")

	filename = './media/voice/' + text.replace(' ', '_')[:24] + str(hash(text)) + '.wav'

	audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

	speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

	print('generating voice')
	speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
	print('voice generated')

	if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
		print("Speech synthesized for text [{}]".format(text))
		return filename
	elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
		cancellation_details = speech_synthesis_result.cancellation_details
		print("Speech synthesis canceled: {}".format(cancellation_details.reason))
		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			if cancellation_details.error_details:
				print("Error details: {}".format(cancellation_details.error_details))
				print("Did you set the speech resource key and region values?")
		return None
