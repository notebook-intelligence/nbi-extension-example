# Copyright (c) Mehmet Bektas <mbektasgh@outlook.com>

from time import sleep
import logging
import uuid
from notebook_intelligence import AnchorData, ButtonData, ChatCommand, HTMLFrameData, MarkdownData, NotebookIntelligenceExtension, Host, ChatParticipant, ChatRequest, ChatResponse, ProgressData, ConfirmationData

from .util import PARTICIPANT_ICON_URL, example_matplotlib_image

log = logging.getLogger(__name__)

class ExampleChatParticipant(ChatParticipant):
    def __init__(self, host: Host):
        super().__init__()
        self.host = host

    @property
    def id(self) -> str:
        return "example"

    @property
    def name(self) -> str:
        return "Example"
    
    @property
    def description(self) -> str:
        return "An example participant"

    @property
    def icon_path(self) -> str:
        return PARTICIPANT_ICON_URL

    @property
    def commands(self) -> list[ChatCommand]:
        return [
            ChatCommand(name='repeat', description='Repeats the prompt'),
            ChatCommand(name='responseTypes', description='Demo response types'),
        ]

    async def handle_chat_request(self, request: ChatRequest, response: ChatResponse, options: dict = {}) -> None:
        request.cancel_token.cancellation_signal.connect(lambda: response.stream(MarkdownData("Cancel event received")))

        if request.command == 'repeat':
            response.stream(MarkdownData(f"Repeating: {request.prompt}"))
            response.finish()
            return
        elif request.command == 'responseTypes':
            for i in range(5):
                response.stream(MarkdownData(f"Hello world {i + 1}!\n\n"))
                if request.cancel_token.is_cancel_requested:
                    log.info("Cancel requested")
                    response.stream(MarkdownData("Cancelled"))
                    response.finish()
                    return
                sleep(0.5)
            
            response.stream(ProgressData("Running..."))
            sleep(2)

            response.stream(MarkdownData("""Here is a Python method I generated. \n```python\ndef show_message():\n  print('Hello world!')\n```\n"""))
            sleep(1)

            response.stream(ButtonData("Button title", "apputils:notify", {
                "message": 'Copilot chat button was clicked',
                "type": 'success',
                "options": { "autoClose": False }
            }))

            response.stream(AnchorData("https://www.jupyter.org", "Click me! I am a link!"))

            response.stream(ProgressData("Generating a matplotlib chart..."))
            sleep(2)
            response.stream(MarkdownData("**Matplotlib chart**"))
            response.stream(HTMLFrameData(f"""
                <div>
                <img style="width: 100%" src="data:image/png;base64,{example_matplotlib_image()}" />
                </div>
                """, height=400))
            
            response.stream(ProgressData("Generating a map..."))
            sleep(2)
            response.stream(MarkdownData("**A map response**"))
            response.stream(HTMLFrameData("""<iframe width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" id="gmap_canvas" src="https://maps.google.com/maps?width=400&amp;height=400&amp;hl=en&amp;q=%20Istanbul+(Istanbul)&amp;t=&amp;z=11&amp;ie=UTF8&amp;iwloc=B&amp;output=embed"></iframe>""", height=400))

            response.finish()
            return

        response.stream(MarkdownData("I don't have a handler for that, transferring request to GitHub Copilot."))
        callback_id = uuid.uuid4().hex
        response.stream(ConfirmationData(
            title="Confirm",
            message="Do you want to transfer to GitHub Copilot?",
            confirmArgs={"id": response.message_id, "data": { "callback_id": callback_id, "data": {"confirmed": True}}},
            cancelArgs={"id": response.message_id, "data": { "callback_id": callback_id, "data": {"confirmed": False}}},
            confirmLabel="Transfer",
            cancelLabel="Cancel"
        ))
        user_input = await ChatResponse.wait_for_chat_user_input(response, callback_id)
        if user_input['confirmed'] == False:
            response.stream(MarkdownData("User cancelled the transfer."))
            response.finish()
            return
        
        await self.host.default_chat_participant.handle_chat_request(request, response, options)

class ExampleExtension(NotebookIntelligenceExtension):
    @property
    def id(self) -> str:
        return "example-extension"

    @property
    def name(self) -> str:
        return "Example Extension"

    @property
    def provider(self) -> str:
        return "Mehmet Bektas"

    @property
    def url(self) -> str:
        return "https://github.com/mbektas"

    def activate(self, host: Host) -> None:
        self.participant = ExampleChatParticipant(host)
        host.register_chat_participant(self.participant)
        log.info("Example extension activated")
