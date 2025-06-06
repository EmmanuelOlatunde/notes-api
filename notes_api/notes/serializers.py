from rest_framework import serializers
from .models import Note, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()  # For output

    class Meta:
        model = Note
        fields = ['owner', 'title', 'content', 'tags']
        read_only_fields = ['owner']

    def get_owner(self, obj):
        return obj.owner.username

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]  # serialize tag names

    def to_internal_value(self, data):
        tags = data.pop('tags', [])  # extract tags from incoming request
        internal = super().to_internal_value(data)
        internal['tags'] = tags
        return internal

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        note = Note.objects.create(owner=self.context['request'].user, **validated_data)
        self._add_tags(note, tags_data)
        return note

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags_data is not None:
            instance.tags.clear()
            self._add_tags(instance, tags_data)
        return instance

    def _add_tags(self, note, tags_data):
        user = self.context['request'].user
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name, owner=user)
            note.tags.add(tag)
