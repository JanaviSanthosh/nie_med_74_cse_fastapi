{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNL6fPkpgEKIb8WiZBJq0U0",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/JanaviSanthosh/nie_med_74_cse_fastapi/blob/main/main.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "rZ1kB3zBqtb9"
      },
      "outputs": [],
      "source": [
        "from fastapi import FastAPI,HTTPException\n",
        "from pydantic import BaseModel\n",
        "app = FastAPI()\n",
        "@app.get(\"/\")\n",
        "def home():\n",
        "    return {\"meesage\": \"Enterprise IT Service Desk -server\"}\n",
        "db = {\n",
        "    1 : {\"id\" : 1, \"title\" : \"computer is not on\",\n",
        "         \"description\" : \"power button is not working\",\n",
        "          \"category\" : \"Hardware\", \"status\" : \"NEW\"},\n",
        "    2 : {\"id\": 2,\"title\": \"internet is not working\",\n",
        "         \"description\" : \"wify problem\",\n",
        "         \"category\" : \"Hardware\", \"status\" : \"NEW\"}\n",
        " }\n",
        "#Schemas\n",
        "class TicketCreate(BaseModel):\n",
        "    title : str\n",
        "    description : str\n",
        "    category :str\n",
        "    status : str\n",
        "\n",
        "class TicketResponse(TicketCreate):\n",
        "    id : int\n",
        "\n",
        "#APIs\n",
        "@app.get(\"/tickets\")\n",
        "def get_tickets():\n",
        "    return list(db.values())\n",
        "\n",
        "@app.get(\"/tickets/{id}\")\n",
        "def get_ticket(id: int):\n",
        "    if id not in db:\n",
        "        raise HTTPException(status_code=404, detail=\"Ticket not found\")\n",
        "    return db[id]\n",
        "\n",
        "\n",
        "\n",
        "@app.post(\"/tickets\", status_code=201, response_model=TicketResponse)\n",
        "def ticket_create(ticket_payload : TicketCreate):\n",
        "        new_id = max(db.keys(), default=0) + 1\n",
        "        db[new_id] = {\"id\" : new_id, **ticket_payload.model_dump()}\n",
        "        return db[new_id]\n",
        "\n",
        "@app.put(\"/tickets/{id}\", response_model=TicketResponse)\n",
        "def tickets_update(id: int, ticket_payload: TicketCreate):\n",
        "    if id not in db:\n",
        "        raise HTTPException(detail=\"Ticket not found\", status_code=404)\n",
        "    db[id] = {\"id\" : id , **ticket_payload.model_dump()}\n",
        "    return db[id]\n",
        "\n",
        "@app.delete(\"/tickets/{id}\")\n",
        "def tickets_delete(id: int):\n",
        "    if id not in db:\n",
        "        raise HTTPException(detail=\"Ticket not found\", status_code=404)\n",
        "    del db[id]\n",
        "    return {\"message\": \"Ticket deleted successfully\"}"
      ]
    }
  ]
}