from firebase_admin import firestore

db = firestore.client()


def create_user(uid, email, display_name, role="client"):
    user_data = {
        "email": email,
        "displayName": display_name,
        "role": role,
        "createdAt": firestore.SERVER_TIMESTAMP
    }
    db.collection("users").document(uid).set(user_data)


def upload_policy(owner_uid, name, file_url, chunk_ids):
    policy = {
        "ownerUid": owner_uid,
        "name": name,
        "fileURL": file_url,
        "chunkIds": chunk_ids,
        "uploadedAt": firestore.SERVER_TIMESTAMP
    }
    db.collection("policies").add(policy) 

def create_pa_request(pa_id, client_uid, provider_id, diagnoses, services, ref):
    pa_data = {
        "clientUid": client_uid,
        "providerId": provider_id,
        "ref": ref,
        "diagnoses": diagnoses,
        "services": services,
        "status": "pending",
        "createdAt": firestore.SERVER_TIMESTAMP
    }
    db.collection("paRequests").document(pa_id).set(pa_data)
    


def create_claim(claim_id, client_uid, provider_id, ref, billed_amount, items):
    claim_data = {
        "clientUid": client_uid,
        "providerId": provider_id,
        "ref": ref,
        "billedAmount": billed_amount,
        "items": items,
        "status": "pending",
        "createdAt": firestore.SERVER_TIMESTAMP
    }
    db.collection("claims").document(claim_id).set(claim_data)


def start_chat(owner_uid, context_ids):
    chat_ref = db.collection("chats").document()
    chat_ref.set({
        "ownerUid": owner_uid,
        "contextIds": context_ids,
        "createdAt": firestore.SERVER_TIMESTAMP
    })
    return chat_ref.id


def send_message(chat_id, sender, text, sources=None):
    message_data = {
        "sender": sender,
        "text": text,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    if sources:
        message_data["sources"] = sources

    db.collection("chats").document(chat_id).collection("messages").add(message_data)

